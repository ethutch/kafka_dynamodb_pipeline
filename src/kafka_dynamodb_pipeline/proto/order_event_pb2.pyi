from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderDetailMessage(_message.Message):
    __slots__ = ("product_id", "unit_price", "quantity", "discount")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    UNIT_PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_FIELD_NUMBER: _ClassVar[int]
    product_id: int
    unit_price: float
    quantity: int
    discount: float
    def __init__(self, product_id: _Optional[int] = ..., unit_price: _Optional[float] = ..., quantity: _Optional[int] = ..., discount: _Optional[float] = ...) -> None: ...

class OrderEventMessage(_message.Message):
    __slots__ = ("correlation_id", "action", "order_id", "customer_id", "employee_id", "order_date", "required_date", "shipped_date", "freight", "ship_name", "ship_address", "ship_city", "ship_region", "ship_postal_code", "ship_country", "order_details", "created_by", "updated_by", "created_at", "updated_at")
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_DATE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_DATE_FIELD_NUMBER: _ClassVar[int]
    SHIPPED_DATE_FIELD_NUMBER: _ClassVar[int]
    FREIGHT_FIELD_NUMBER: _ClassVar[int]
    SHIP_NAME_FIELD_NUMBER: _ClassVar[int]
    SHIP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SHIP_CITY_FIELD_NUMBER: _ClassVar[int]
    SHIP_REGION_FIELD_NUMBER: _ClassVar[int]
    SHIP_POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    SHIP_COUNTRY_FIELD_NUMBER: _ClassVar[int]
    ORDER_DETAILS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    correlation_id: str
    action: str
    order_id: int
    customer_id: str
    employee_id: int
    order_date: str
    required_date: str
    shipped_date: str
    freight: float
    ship_name: str
    ship_address: str
    ship_city: str
    ship_region: str
    ship_postal_code: str
    ship_country: str
    order_details: _containers.RepeatedCompositeFieldContainer[OrderDetailMessage]
    created_by: str
    updated_by: str
    created_at: int
    updated_at: int
    def __init__(self, correlation_id: _Optional[str] = ..., action: _Optional[str] = ..., order_id: _Optional[int] = ..., customer_id: _Optional[str] = ..., employee_id: _Optional[int] = ..., order_date: _Optional[str] = ..., required_date: _Optional[str] = ..., shipped_date: _Optional[str] = ..., freight: _Optional[float] = ..., ship_name: _Optional[str] = ..., ship_address: _Optional[str] = ..., ship_city: _Optional[str] = ..., ship_region: _Optional[str] = ..., ship_postal_code: _Optional[str] = ..., ship_country: _Optional[str] = ..., order_details: _Optional[_Iterable[_Union[OrderDetailMessage, _Mapping]]] = ..., created_by: _Optional[str] = ..., updated_by: _Optional[str] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ...) -> None: ...
