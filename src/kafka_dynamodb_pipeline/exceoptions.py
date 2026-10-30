"""Exceptions for deserializing the Kafka messages in the Kafka-DynamoDB pipeline."""


class MapperError(ValueError):
    """Base for all event ValueErrors."""

class UnsupportedEventVersionError(MapperError):
    """Raised when an action is not supported by the mapper."""

class EventTypeError(MapperError):
    """Raised when an event has an invalid or unsupported type."""

class MissingEventError(MapperError):
    """Raised when an event required by the mapper is missing."""

class CustomerIdError(MapperError):
    """Raised when a customer_id is missing or invalid."""