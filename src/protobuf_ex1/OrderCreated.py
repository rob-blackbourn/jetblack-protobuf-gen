from typing import Mapping, TypedDict, Unpack, overload

from .pb import events_pb2

from .serializable import Serializable, MessageMeta


class OrderCreated(Serializable, metaclass=MessageMeta, message_type=events_pb2.OrderCreated):

    class Kwargs(TypedDict):
        order_id: str
        symbol: str
        quantity: int

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
