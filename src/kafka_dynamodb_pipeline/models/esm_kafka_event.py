from pydantic import BaseModel, ConfigDict, Field


class ESMKafkaRecord(BaseModel):
    """One record in an AWS Lambda Kafka ESM event."""

    model_config = ConfigDict(extra="allow")

    topic: str
    partition: int
    offset: int
    timestamp: int
    timestamp_type: str = Field(alias="timestampType")

    key: str | None = None
    value: str
    headers: list[dict[str, list[int]]] = Field(default_factory=list)


class ESMKafkaEvent(BaseModel):
    """AWS Lambda Self-Managed Kafka event envelope."""

    model_config = ConfigDict(extra="allow")

    event_source: str = Field(
        alias="eventSource"
    )
    bootstrap_servers: str = Field(alias="bootstrapServers")
    records: dict[str, list[ESMKafkaRecord]]
