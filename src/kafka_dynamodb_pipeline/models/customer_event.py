from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator

from kafka_dynamodb_pipeline.config.settings import get_settings
from kafka_dynamodb_pipeline.models.processing_result import ProcessingResult

settings = get_settings()

class CustomerEvent(ProcessingResult):
    """Domain wrapper for CustomerEventMessage with Kafka and Mongo capabilities."""

    correlation_id: str = Field(
        default="", 
        description="Unique identifier for the event"
    )
    action: str = Field(
        default="", 
        description="CRUD Action to be performed, e.g., 'CREATE', 'UPDATE', 'DELETE'"
    )
    customer_id: str = Field(
        default="",
        description="Unique identifier for the customer, used as the partition key in DynamoDB",
    )
    company_name: str = Field(
        default="", 
        description="Name of the customer's company"
    )
    contact_name: str | None = Field(
        default=None, 
        description="Name of the customer's contact person"
    )
    contact_title: str | None = Field(
        default=None, 
        description="Title of the customer's contact person"
    )
    address: str | None = Field(
        default=None, 
        description="Customer's address")
    city: str | None = Field(
        default=None, 
        description="Customer's city")
    region: str | None = Field(
        default=None, 
        description="Customer's region or state")
    postal_code: str | None = Field(
        default=None, 
        description="Customer's postal code")
    country: str | None = Field(
        default=None, 
        description="Customer's country")
    phone: str | None = Field(
        default=None, 
        description="Customer's phone number")
    fax: str | None = Field(
        default=None, 
        description="Customer's fax number")
    created_by: str | None = Field(
        default=None, 
        description="User who created the customer record")
    updated_by: str | None = Field(
        default=None, description="User who updated the customer record")
    created_at: datetime | None = Field(
        default=None, 
        description="Timestamp of when the customer record was created"
    )
    updated_at: datetime | None = Field(
        default=None, 
        description="Timestamp of when the customer record was last updated"
    )

    def is_success(self) -> bool:
        return True

    def get_event_type(self) -> str:
        return "CUSTOMER"

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        s = v.strip().upper()
        if not s:
            raise ValueError("action cannot be empty")
        return s

    @field_validator("customer_id")
    @classmethod
    def validate_customer_id(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("customer_id cannot be empty, GS1 requires a non-empty string "
                             "for the customer_id.")
        return s[:5]

