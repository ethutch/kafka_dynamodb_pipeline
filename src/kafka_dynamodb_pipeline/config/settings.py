"""Application configuration — loaded from environment variables / .env file."""

from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class DynamoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DYNAMODB_", env_file=".env", extra="ignore")

    endpoint_url: str | None = Field(
        default=None, description="Custom endpoint for local DynamoDB container"
    )
    table_name: str = Field(default="customers", description="Target DynamoDB table name")
    region_name: str = Field(default="us-east-1", description="AWS Region")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    environment: str = Field(default="local", description="Runtime environment")
    batch_size: int = Field(default=100, description="Max batch size")
    batch_timeout_ms: int = Field(default=5000, description="Max batch timeout in ms")
    aws_region: str = Field(default="us-east-1", description="AWS Region")

    dynamodb: DynamoDBSettings = Field(default_factory=DynamoDBSettings)

    supported_customer_events: Annotated[set[int], NoDecode] | None = None
    supported_order_events: Annotated[set[int], NoDecode] = Field(
    default_factory=set,
    validation_alias="SUPPORTED_ORDER_EVENTS",
    )

    @field_validator("supported_customer_events", "supported_order_events", mode="before")
    @classmethod
    def decode_supported_events(cls, v: str | Sequence[int]) -> set[int]:
        if isinstance(v, str):
            return {int(x.strip()) for x in v.split(",") if x.strip()}
        if isinstance(v, (list, tuple, set)):
            return {int(x) for x in v if x}
        return set()


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return a cached singleton of AppSettings."""
    return AppSettings()
