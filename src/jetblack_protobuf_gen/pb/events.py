from typing import Mapping, TypedDict, Unpack, overload

from jetblack_protobuf_gen.pb import events_pb2

from jetblack_protobuf_gen.serializable import Serializable, MessageMeta


class OrderCreated(
    Serializable[events_pb2.OrderCreated],
    metaclass=MessageMeta,
    message_type=events_pb2.OrderCreated
):

    order_id: str
    symbol: str
    quantity: int

    class Kwargs(TypedDict):
        order_id: str
        symbol: str
        quantity: int


    @overload
    def __init__(
            self,
            instance: events_pb2.OrderCreated,
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


    trade_id: str
    order_id: str
    fills: list[Serializable]

    class Kwargs(TypedDict):
        trade_id: str
        order_id: str
        fills: list[Serializable]


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
        "jetblack_protobuf_gen.pb.TradeExecuted.Fill": Fill
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

