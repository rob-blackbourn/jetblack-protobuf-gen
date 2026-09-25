from __future__ import annotations

from typing import Any, Mapping, cast, overload

from google.protobuf.internal import containers
from google.protobuf import descriptor
from google.protobuf.message import Message
from google.protobuf import any_pb2


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
        dct['MESSAGE_FIELDS'] = {
            field.name: field
            for field in message_type.DESCRIPTOR.fields
        }
        return super().__new__(cls, name, bases, dct)


class Serializable[MessageType: Message]:
    __slots__ = ('_instance', '_lists', '_messages', '_is_finalized')

    MESSAGE_TYPE: type[MessageType]
    MESSAGE_FIELDS: dict[str, descriptor.FieldDescriptor]

    @overload
    def __init__(
        self,
        instance: Message,
        serializables: Mapping[str, type[Serializable]],
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
        self._lists: dict[str, list[Any]] = {}
        self._messages: dict[str, Serializable | None] = {}

        if args:
            self._instance, serializables = cast(
                tuple[MessageType, Mapping[str, type[Serializable]]],
                args
            )

            self._is_finalized = True

            for field in self._instance.DESCRIPTOR.fields:

                value = getattr(self._instance, field.name)

                if field.type == field.TYPE_MESSAGE:
                    if isinstance(value, any_pb2.Any):
                        type_name = value.TypeName()
                    else:
                        assert field.message_type is not None
                        type_name = field.message_type.full_name
                    serializable_type = serializables[type_name]
                    if field.is_repeated:
                        self._lists[field.name] = [
                            serializable_type(item, serializables)
                            for item in value
                        ]
                    else:
                        self._messages[field.name] = serializable_type(
                            value, serializables)
                else:
                    if field.is_repeated:
                        self._lists[field.name] = list(value)
        else:
            self._instance = self.MESSAGE_TYPE()
            self._is_finalized = False
            for field in self._instance.DESCRIPTOR.fields:
                value = kwargs.get(field.name)
                if value is None:
                    if field.is_repeated:
                        self._lists[field.name] = []
                    elif field.type == field.TYPE_MESSAGE:
                        self._messages[field.name] = None
                else:
                    if isinstance(value, Serializable):
                        self._messages[field.name] = value
                    elif isinstance(value, list):
                        self._lists[field.name] = value
                    else:
                        setattr(self._instance, field.name, value)

    def __getattr__(self, name: str) -> Any:
        if not name in self.MESSAGE_FIELDS:
            return super().__getattribute__(name)
        elif name in self._lists:
            return self._lists[name]
        elif name in self._messages:
            return self._messages[name]
        else:
            return getattr(self._instance, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if not name in self.MESSAGE_FIELDS:
            return super().__setattr__(name, value)

        self._is_finalized = False

        if name in self._lists:
            self._lists[name] = value
        elif name in self._messages:
            self._messages[name] = value
        else:
            setattr(self._instance, name, value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Serializable):
            return NotImplemented
        return self.finalize() == other.finalize()

    def finalize(self) -> MessageType:
        if self._is_finalized:
            return self._instance

        for field in self._instance.DESCRIPTOR.fields:
            if field.type == field.TYPE_MESSAGE:
                value = getattr(self._instance, field.name)
                if field.is_repeated:
                    value = cast(
                        containers.RepeatedCompositeFieldContainer,
                        value
                    )
                    for item in cast(list[Serializable], self._lists[field.name]):
                        instance = cast(Message, value.add())
                        instance.CopyFrom(item.finalize())
                else:
                    value = cast(Message, value)
                    message = self._messages[field.name]
                    if message is not None:
                        value.CopyFrom(message.finalize())
            elif field.is_repeated:
                repeated_values = cast(
                    containers.RepeatedScalarFieldContainer,
                    getattr(self._instance, field.name)
                )
                for item in self._lists[field.name]:
                    repeated_values.append(item)

        self._is_finalized = True

        return self._instance

    def to_binary(self) -> bytes:
        return self.finalize().SerializeToString()

    @classmethod
    def from_binary(
            cls,
            buf: bytes,
            serializables: Mapping[str, type[Serializable]] | None = None
    ) -> Serializable[MessageType]:
        instance = cls.MESSAGE_TYPE.FromString(buf)
        return cls(instance, serializables or {})
