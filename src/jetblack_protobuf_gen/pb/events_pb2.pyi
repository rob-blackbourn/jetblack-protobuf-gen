from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Side(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIDE_UNSPECIFIED: _ClassVar[Side]
    SIDE_BUY: _ClassVar[Side]
    SIDE_SELL: _ClassVar[Side]
SIDE_UNSPECIFIED: Side
SIDE_BUY: Side
SIDE_SELL: Side

class OrderCreated(_message.Message):
    __slots__ = ("order_id", "symbol", "quantity")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    symbol: str
    quantity: int
    def __init__(self, order_id: _Optional[str] = ..., symbol: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class TradeExecuted(_message.Message):
    __slots__ = ("trade_id", "order_id", "fills")
    class Counterparty(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COUNTERPARTY_UNSPECIFIED: _ClassVar[TradeExecuted.Counterparty]
        COUNTERPARTY_INTERNAL: _ClassVar[TradeExecuted.Counterparty]
        COUNTERPARTY_EXTERNAL: _ClassVar[TradeExecuted.Counterparty]
    COUNTERPARTY_UNSPECIFIED: TradeExecuted.Counterparty
    COUNTERPARTY_INTERNAL: TradeExecuted.Counterparty
    COUNTERPARTY_EXTERNAL: TradeExecuted.Counterparty
    class Fill(_message.Message):
        __slots__ = ("fill_id", "quantity", "price")
        FILL_ID_FIELD_NUMBER: _ClassVar[int]
        QUANTITY_FIELD_NUMBER: _ClassVar[int]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        fill_id: str
        quantity: int
        price: float
        def __init__(self, fill_id: _Optional[str] = ..., quantity: _Optional[int] = ..., price: _Optional[float] = ...) -> None: ...
    TRADE_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    FILLS_FIELD_NUMBER: _ClassVar[int]
    trade_id: str
    order_id: str
    fills: _containers.RepeatedCompositeFieldContainer[TradeExecuted.Fill]
    def __init__(self, trade_id: _Optional[str] = ..., order_id: _Optional[str] = ..., fills: _Optional[_Iterable[_Union[TradeExecuted.Fill, _Mapping]]] = ...) -> None: ...
