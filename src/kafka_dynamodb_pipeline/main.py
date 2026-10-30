"""Lambda consumer entrypoint for Kafka event processing."""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Any

import boto3
from google.protobuf.message import DecodeError
from pydantic import ValidationError

from kafka_dynamodb_pipeline import EventDeserializer
from kafka_dynamodb_pipeline.config import get_settings
from kafka_dynamodb_pipeline.models.esm_kafka_event import ESMKafkaEvent
from kafka_dynamodb_pipeline.models.processing_result import ProcessingResult
from kafka_dynamodb_pipeline.utils import configure_logging, get_logger

if TYPE_CHECKING:
    from aws_lambda_typing.context import Context
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

configure_logging()
log = get_logger(__name__)
event_deserializer = EventDeserializer()

def get_dynamodb_table() -> Table:
    '''Get a DynamoDB table resource using settings from the environment or .env file.'''
    settings = get_settings()
    dynamodb_kwargs: dict[str, Any] = {
        "region_name": settings.aws_region,
        "endpoint_url": settings.dynamodb.endpoint_url,
    }

    dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb", **dynamodb_kwargs)
    return dynamodb.Table(settings.dynamodb.table_name)


def handler(event: dict[str, Any], context: Context) -> dict[str, Any]:  
    '''AWS Lambda handler function to process Kafka events and store them in DynamoDB.'''

    esm_kafka_event = ESMKafkaEvent.model_validate(event)

    batch_item_failures = []
    processed_count = 0
    error_count = 0
    table = get_dynamodb_table()

    for partition_key, record_list in esm_kafka_event.records.items():
        log.debug("partition.processing_started", partition=partition_key, count=len(record_list))
        for record in record_list:
            try:
                raw_bytes: bytes = base64.b64decode(record.value)
               
                domain_event: ProcessingResult = event_deserializer.process(record, raw_bytes)
                log.debug("Event Deserialized ", domain_event.model_dump())

                # Convert to DynamoDB 
                item = domain_event.model_dump(by_alias=True, mode="json")  
                #TODO: Take proper action based on the event type (CREATE, UPDATE, DELETE)

                table.put_item(Item=item)
                log.info(
                    "record.persistence_succeeded",
                    customer_id=item.get("customer_id"),
                    table_name=table.name,
                )
                processed_count += 1

            except (DecodeError, ValidationError) as err:
                log.error("record.deserialization_failed", error=err, record=record)
                error_count += 1
                batch_item_failures.append(
                    {
                        "itemIdentifier": {
                        "partition": f"{record.topic}-{record.partition}",
                        "offset": int(record.offset),
                        }
                    }
                )
            except Exception as ex:
                log.critical("record.persistence_failed", error=str(ex), exc_info=True)
                error_count += 1
                batch_item_failures.append(
                    {
                        "itemIdentifier": {
                        "partition": f"{record.topic}-{record.partition}",
                        "offset": int(record.offset),
                        }
                    }
                )

    return {"batchItemFailures:": batch_item_failures}
