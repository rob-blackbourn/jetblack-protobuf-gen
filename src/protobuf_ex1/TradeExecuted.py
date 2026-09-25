from typing import Mapping, Self, TypedDict, Unpack, overload

from .pb import events_pb2

from .serializable import Serializable, MessageMeta


class TradeExecuted(
    Serializable[events_pb2.TradeExecuted],
    metaclass=MessageMeta,
    message_type=events_pb2.TradeExecuted
):

    class Fill(
        Serializable[events_pb2.TradeExecuted.Fill],
        metaclass=MessageMeta,
        message_type=events_pb2.TradeExecuted.Fill
    ):

        fill_id: str
        quantity: int
        price: float

        class Kwargs(TypedDict):
            fill_id: str
            quantity: int
            price: float

        @overload
        def __init__(
                self,
                instance: events_pb2.TradeExecuted.Fill,
                serializables: Mapping[str, Serializable]
        ) -> None:
            ...

        @overload
        def __init__(
                self,
                **kwargs: Unpack[Kwargs]
        ) -> None:
            ...

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

    order_id: str
    trade_id: str
    fills: list[Fill]

    class Kwargs(TypedDict):
        order_id: str
        trade_id: str
        fills: list[TradeExecuted.Fill]

    @overload
    def __init__(
            self,
            instance: events_pb2.TradeExecuted,
            serializables: Mapping[str, Serializable]
    ) -> None:
        ...

    @overload
    def __init__(
            self,
            **kwargs: Unpack[Kwargs]
    ) -> None:
        ...

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    _KNOWN_SERIALIZABLES: Mapping[str, type[Serializable]] = {
        events_pb2.TradeExecuted.Fill.DESCRIPTOR.full_name: Fill
    }

    @classmethod
    def from_binary(
            cls,
            buf: bytes,
            serializables: Mapping[str, type[Serializable]] | None = None
    ) -> Serializable[events_pb2.TradeExecuted]:
        if serializables is None:
            serializables = cls._KNOWN_SERIALIZABLES
        elif any(x not in serializables for x in cls._KNOWN_SERIALIZABLES):
            serializables = dict(serializables).update(
                cls._KNOWN_SERIALIZABLES
            )

        return super().from_binary(buf, serializables)
