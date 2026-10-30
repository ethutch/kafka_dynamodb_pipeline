
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ProcessingResult(BaseModel):
    """Interface for all processing outcomes"""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    ) 


    kafka_topic: str
    kafka_partition: int
    kafka_offset: int
    ingested_at: datetime = Field(
        alias="ingestedAt",
        default_factory=lambda: datetime.now(tz=UTC)
    ) 

    def is_success(self) -> bool:
        # Enforces that every subclass must implement this explicitly
        raise NotImplementedError("Subclasses must implement is_success()")

    def get_event_type(self) -> str:
        raise NotImplementedError("Subclasses must implement get_event_type()")

    def to_dynamodb_item(self) -> dict[str, Any]:
        """Serialize the event using aliases and bundle Kafka metadata."""
        
        document = self.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude={"kafka_partition", "kafka_offset",},
        )

        document["_meta"] = {
            "topic": document.pop("kafkaTopic"),
            "ingestedAt": document.pop("ingestedAt"),
        }

        document["_id"] = document.pop("correlationId")
        return document