from typing import Mapping, Protocol, TypedDict, Unpack, cast, overload

from google.protobuf.message import Message

from protobuf_ex1.pb import events_pb2


class MessageMeta[T: type](type):
    MESSAGE_TYPE = type[Message]

    def __new__(
            cls: T,
            name: str,
            bases: tuple[type],
            dct: dict,
            message_type: type[Message]
    ) -> T:
        dct['MESSAGE_TYPE'] = message_type
        return super().__new__(cls, name, bases, dct)


class ISerializable[MessageType: Message](Protocol):

    @overload
    def __init__(
        self,
        instance: Message,
        serializablse: Mapping[str, Message],
        /
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        **kwargs
    ) -> None:
        ...

    def __init__(self, *args, **kwargs) -> None:
        ...

    def finalize(self) -> MessageType:
        ...

    def to_binary(self) -> bytes:
        ...

    @classmethod
    def from_binary(
            cls,
            buf: bytes,
            serializables: Mapping[str, ISerializable] | None = None
    ) -> ISerializable[MessageType]:
        ...


class Serializable[MessageType: Message](ISerializable[MessageType]):
    pass


def make_serializable[MessageType: Message](message_type: type[MessageType]) -> type[Serializable[MessageType]]:

    Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})

    class _Serializable(metaclass=MessageMeta, message_type=message_type):

        @overload
        def __init__(
            self,
            instance: Message,
            serializablse: Mapping[str, Message],
            /
        ) -> None:
            ...

        @overload
        def __init__(
            self,
            **kwargs: Unpack[Point2D]
        ) -> None:
            ...

        def __init__(self, *args, **kwargs) -> None:
            if args:
                self._instance, serializables = cast(
                    tuple[str, Serializable], args
                )

        def finalize(self) -> MessageType:
            raise NotImplementedError()

        def to_binary(self) -> bytes:
            raise NotImplementedError()

        @classmethod
        def from_binary(
                cls,
                buf: bytes,
                serializables: Mapping[str, Serializable] | None = None
        ) -> Serializable[MessageType]:
            raise NotImplementedError()

    return _Serializable


TradeExecuted = make_serializable(events_pb2.TradeExecuted)
OrderCreated = make_serializable(events_pb2.OrderCreated)


def main() -> None:
    trade_executed = TradeExecuted()
    order_created = OrderCreated()
    print("Here")


if __name__ == "__main__":
    main()
