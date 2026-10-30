import pytest
from pydantic import ValidationError

from kafka_dynamodb_pipeline.models.customer_event import CustomerEvent
from kafka_dynamodb_pipeline.proto.customer_event_pb2 import CustomerEventMessage


def test_customer_id_validation_truncates_and_rejects_empty() -> None:
    event = CustomerEvent(
        customer_id="ALFKI_EXTRA", 
        company_name="Alfreds Futterkiste",
        kafka_topic="customer_events",
        kafka_partition=0,
        kafka_offset=0,
    )
    assert event.customer_id == "ALFKI"

    with pytest.raises(ValidationError):
        CustomerEvent(customer_id="   ", 
                      company_name="Invalid Customer",
                      kafka_topic="customer_events",
                      kafka_partition=0,
                      kafka_offset=0,
        )
