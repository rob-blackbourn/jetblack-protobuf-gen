from typing import Mapping, overload

from google.protobuf.message import Message


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
        cls.foo = "hello"
        return super().__new__(cls, name, bases, dct)


class SerializableFactory:

    def __init__(self, message_type: type[Message]) -> None:
        self._message_type = message_type

    @overload
    def __call__(
        self,
        instance: Message,
        serializablse: Mapping[str, Message],
        /
    ) -> Serializable:
        ...

    @overload
    def __call__(
        self,
        **kwargs
    ) -> Serializable:
        ...

    def __call__(self, *args, **kwargs) -> Serializable:
        raise NotImplementedError()


class Serializable:
    pass
