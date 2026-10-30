from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from kafka_dynamodb_pipeline.models.processing_result import ProcessingResult


def ms_to_datetime(epoch_ms: int) -> datetime | None:
    if not epoch_ms:
        return None
    return datetime.fromtimestamp(epoch_ms / 1000.0, tz=UTC)

class OrderDetail(BaseModel):
    """Nested domain representation of an itemized order line."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )

    product_id: int = Field(
        default=0, description="Unique identifier for the product"
    )
    unit_price: float = Field(
        default=0.0, description="Price per unit of the product"
    )
    quantity: int = Field(
        default=0, description="Number of units ordered")
    discount: float = Field(
        default=0.0, description="Discount applied to the order line"
    )


class OrderEvent(ProcessingResult):
    """Domain wrapper for OrderEventMessage with Kafka and Mongo capabilities."""

    correlation_id: str = Field(
        default="", 
        description="Unique identifier for the event"
    )
    action: str = Field(
        default="", 
        description="CRUD Action to be performed, e.g., 'CREATE', 'UPDATE', 'DELETE'"
    )
    order_id: int = Field(
        default=0, 
        description="Unique identifier for the order"
    )
    customer_id: str = Field(
        default="", 
        description="Unique identifier for the customer"
    )
    employee_id: int = Field(
        default=0, 
        description="Unique identifier for the employee"
    )
    order_date: str = Field(
        default="", 
        description="Date the order was placed"
    )
    required_date: str = Field(
        default="", description="Date the order is required"
    )
    shipped_date: str = Field(
        default="", 
        description="Date the order was shipped"
    )
    freight: float = Field(
        default=0.0, 
        description="Shipping cost for the order"
    )
    ship_name: str = Field(
        default="", 
        description="Name of the shipping recipient"
    )
    ship_address: str = Field(
        default="", description="Shipping address for the order"
    )
    ship_city: str = Field(
        default="", 
        description="City for the shipping address"
    )
    ship_region: str = Field(
        default="", 
        description="Region or state for the shipping address"
    )
    ship_postal_code: str = Field(
        default="", 
        description="Postal code for the shipping address"
    )
    ship_country: str = Field(
        default="", 
        description="Country for the shipping address"
    )
    order_details: list[OrderDetail] = Field(
        default_factory=list)
    
    created_by: str = Field(
        default="", 
        description="User who created the order"
    )
    updated_by: str = Field(
        default="", 
        description="User who last updated the order"
    )
    created_at: datetime | None = Field(
        default=None,
        description="Timestamp when the order was created"
    )
    updated_at: datetime | None = Field(
        default=None, 
        description="Timestamp when the order was last updated"
    )

    def is_success(self) -> bool:
        return True

    def get_event_type(self) -> str:
        return "ORDER"
