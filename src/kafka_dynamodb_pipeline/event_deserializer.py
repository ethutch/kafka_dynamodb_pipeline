from __future__ import annotations

import struct
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, NamedTuple

from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message

from kafka_dynamodb_pipeline.config.settings import get_settings
from kafka_dynamodb_pipeline.models import CustomerEvent, OrderEvent, ProcessingResult
from kafka_dynamodb_pipeline.models.esm_kafka_event import ESMKafkaRecord
from kafka_dynamodb_pipeline.proto import customer_event_pb2, order_event_pb2
from kafka_dynamodb_pipeline.utils import get_logger

log = get_logger(__name__)

# Apicurio 2.x magic byte that starts every serialised message
_APICURIO_MAGIC_BYTE = 0x00
_APICURIO_HEADER_LENGTH = 9 
_APICURIO_MIN_MESSAGE_LENGTH = 10

class EventDeserializer:
    def __init__(self) -> None:
        settings = get_settings()
        
        self.supported_customer_events = settings.supported_customer_events
        self.supported_order_events = settings.supported_order_events
        log.debug("ApicurioProcessor initialized",
                    supported_customer_events=self.supported_customer_events,
                    supported_order_events=self.supported_order_events)
        
        # Bind the class constructors directly to self so Python avoids module lookups in the loop
        self._customer_proto_factory = customer_event_pb2.CustomerEventMessage
        self._order_proto_factory = order_event_pb2.OrderEventMessage


    def process(self, esm_kafka_record: ESMKafkaRecord, wire_payload: bytes) -> ProcessingResult:
 
         # First strip off the apicurio header    
        log.debug("Process message Strip apicurio header", topic=esm_kafka_record.topic, 
                  payload=wire_payload)
        payload: Payload = self._strip_apicurio_header(wire_payload) 
        
        # Remove protobuf encoding and handle Customer Events
        if esm_kafka_record.topic == "customer-events": 
            if (self.supported_customer_events is not None and
                 payload.schema_id in self.supported_customer_events):
             
                return self._deserialize_and_build_event(
                    esm_kafka_record=esm_kafka_record,
                    payload=payload,
                    proto_factory=self._customer_proto_factory,  # Passes the pre-bound factory
                    target_event_class=CustomerEvent
                )
            else:        
                log.warning(
                    f"Unsupported schema ID:{payload.schema_id} for topic:{esm_kafka_record.topic}"
                )
                raise ValueError(
                    f"Unsupported schema ID: {payload.schema_id} for topic: "
                    f"{esm_kafka_record.topic}"
                )
        
        # Remove protobuf encoding and handle Order Events
        elif esm_kafka_record.topic == "order-events":
            if (self.supported_order_events is not None and
                 payload.schema_id in self.supported_order_events):
                return self._deserialize_and_build_event(
                    esm_kafka_record=esm_kafka_record,
                    payload=payload,
                    proto_factory=self._order_proto_factory,  # Passes the pre-bound factory 
                    target_event_class=OrderEvent
                )
            else:        
                raise ValueError(
                    f"Unsupported schema ID:{payload.schema_id} for topic:{esm_kafka_record.topic}"
                 )
        # No telling what we got.
        else:
            raise ValueError(f"Received message for unsupported topic: {esm_kafka_record.topic}")


    def _deserialize_and_build_event(
        self,
        esm_kafka_record: ESMKafkaRecord,
        payload: Payload,
        proto_factory: Callable[[], Message],
        target_event_class: type[ProcessingResult]
    ) -> ProcessingResult:
        """
        Dynamically decodes a protobuf payload and constructs the matching Pydantic domain event.
        
        Args:
            esm_kafka_record:   The original ESMKafkaRecord containing topic/partition/offset 
                                metadata.
            payload:            The raw protobuf bytes from the message after stripping the 
                                Apicurio header.
            proto_factory:      Callable returning a new instance of the correct Protobuf message 
                                class.
            target_event_class: The Pydantic domain model class to instantiate on successful
                                decoding (e.g., CustomerEvent)."""
    
        # Dynamically grab the class name for clean error logging
        class_name = target_event_class.__name__
    
        try:
            # 1. Instantiate the correct Protobuf container via passed factory
            proto_instance: Message = proto_factory()
            proto_instance.ParseFromString(payload.message)

            # 2. Convert to standard dict
            event_dict: dict[str, Any] = MessageToDict(
                proto_instance,
                preserving_proto_field_name=True,
                always_print_fields_with_no_presence=True 
            )

            # 3. Inject shared infrastructure metadata
            event_dict["kafka_topic"] = esm_kafka_record.topic
            event_dict["kafka_partition"] = esm_kafka_record.partition
            event_dict["kafka_offset"] = esm_kafka_record.offset
            event_dict["ingested_at"] = datetime.now(tz=UTC)

            # 4. Instantiate the passed Pydantic domain class (e.g., CustomerEvent)
            return target_event_class(**event_dict)

        except Exception:
            log.error(f"Protobuf failed to deserialize {class_name}")
            raise

    @staticmethod
    def _strip_apicurio_header(value: bytes) -> Payload:
        """
        Validate and strip the Apicurio 2.x wire format header.

        Returns:
            Payload(proto_bytes, schema_id)

        Raises:
            ValueError if the magic byte is missing (message not Apicurio-encoded)
        """
        if len(value) < _APICURIO_MIN_MESSAGE_LENGTH:
            raise ValueError(
                f"Message too short to contain Apicurio header: {len(value)} bytes"
            )
        magic = value[0]
        if magic != _APICURIO_MAGIC_BYTE:
            raise ValueError(
                f"Missing Apicurio magic byte — expected 0x00, got {hex(magic)}. "
                f"Message may not be Apicurio-encoded."
            )
        schema_id: int = struct.unpack(">Q", value[1:9])[0]
        proto_bytes = value[_APICURIO_HEADER_LENGTH:]
        return Payload(schema_id=schema_id, message=proto_bytes)

    
class Payload(NamedTuple):
    schema_id: int
    message: bytes

