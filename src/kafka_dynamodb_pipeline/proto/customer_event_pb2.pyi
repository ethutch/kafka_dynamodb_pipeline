import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CustomerEventMessage(_message.Message):
    __slots__ = (
        "correlation_id",
        "action",
        "customer_id",
        "company_name",
        "contact_name",
        "contact_title",
        "address",
        "city",
        "region",
        "postal_code",
        "country",
        "phone",
        "fax",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_TITLE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    FAX_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    correlation_id: str
    action: str
    customer_id: str
    company_name: str
    contact_name: str
    contact_title: str
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    phone: str
    fax: str
    created_by: str
    updated_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        correlation_id: _Optional[str] = ...,
        action: _Optional[str] = ...,
        customer_id: _Optional[str] = ...,
        company_name: _Optional[str] = ...,
        contact_name: _Optional[str] = ...,
        contact_title: _Optional[str] = ...,
        address: _Optional[str] = ...,
        city: _Optional[str] = ...,
        region: _Optional[str] = ...,
        postal_code: _Optional[str] = ...,
        country: _Optional[str] = ...,
        phone: _Optional[str] = ...,
        fax: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        updated_by: _Optional[str] = ...,
        created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
