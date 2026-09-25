from textwrap import indent

from google.protobuf.descriptor_pb2 import (
    DescriptorProto,
    FileDescriptorProto,
    FieldDescriptorProto
)
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer


def to_ultimate_python_type(field: FieldDescriptorProto) -> str:
    match field.type:
        case field.TYPE_BOOL:
            return "bool"
        case field.TYPE_BYTES:
            return "bytes"
        case field.TYPE_FLOAT | field.TYPE_DOUBLE:
            return "float"
        case (
            field.TYPE_FIXED32 | field.TYPE_FIXED64 |
            field.TYPE_INT32 | field.TYPE_INT64 |
            field.TYPE_SFIXED32 | field.TYPE_SFIXED64 |
            field.TYPE_UINT32 | field.TYPE_UINT64
        ):
            return 'int'
        case field.TYPE_STRING:
            return 'str'
        case field.TYPE_MESSAGE:
            return 'Serializable'
        case _:
            raise ValueError(f"Unable to handle: {field.type}")


def to_python_type(field: FieldDescriptorProto) -> str:
    ultimate_type = to_ultimate_python_type(field)
    if field.label == field.LABEL_REPEATED:
        ultimate_type = f"list[{ultimate_type}]"
    return ultimate_type


def generate_known_serializables(
        qualname: str,
        nested_types: RepeatedCompositeFieldContainer[DescriptorProto],
        level: int
) -> str:
    text = ",\n".join(
        f"\"{qualname}.{descriptor.name}\": {descriptor.name}"
        for descriptor in nested_types
    )
    return indent(text, " " * level)


def generate_from_binary(
        qualname: str,
        module: str,
        descriptor: DescriptorProto,
        level: int
) -> str:
    if len(descriptor.nested_type) == 0:
        return ""

    text = f"""\
    _KNOWN_SERIALIZABLES: Mapping[str, type[Serializable]] = {{
        {generate_known_serializables(qualname, descriptor.nested_type, level)}
    }}

    @classmethod
    def from_binary(
            cls,
            buf: bytes,
            serializables: Mapping[str, type[Serializable]] | None = None
    ) -> Serializable[{module}]:
        if serializables is None:
            serializables = cls._KNOWN_SERIALIZABLES
        elif any(x not in serializables for x in cls._KNOWN_SERIALIZABLES):
            serializables = dict(serializables).update(
                cls._KNOWN_SERIALIZABLES
            )

        return super().from_binary(buf, serializables)

"""
    return indent(text, " " * level)


def generate_instance_types(
        fields: RepeatedCompositeFieldContainer[FieldDescriptorProto],
        level: int
) -> str:

    text = "\n".join(
        f"{field.name}: {to_python_type(field)}"
        for field in fields
    )
    return indent(text, " " * level)


def generate_kwargs(
        fields: RepeatedCompositeFieldContainer[FieldDescriptorProto],
        level: int
) -> str:
    text = f"""\
class Kwargs(TypedDict):
{generate_instance_types(fields, level)}
"""
    return indent(text, " " * level)


def generate_class(
        qualname: str,
        module: str,
        descriptor: DescriptorProto,
        level: int
) -> str:
    module = f"{module}.{descriptor.name}"
    qualname = f"{qualname}.{descriptor.name}"
    text = f"""\
class {descriptor.name}(
    Serializable[{module}],
    metaclass=MessageMeta,
    message_type={module}
):
{generate_classes(qualname, module, descriptor.nested_type, 4)}
{generate_instance_types(descriptor.field, 4)}

{generate_kwargs(descriptor.field, 4)}

    @overload
    def __init__(
            self,
            instance: {module},
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

{generate_from_binary(qualname, module, descriptor, level)}"""

    return indent(text, " " * level)


def generate_classes(
        qualname: str,
        module: str,
        message_types: RepeatedCompositeFieldContainer[DescriptorProto],
        level: int
) -> str:
    if len(message_types) == 0:
        return ""

    text = "\n".join(
        generate_class(qualname, module, descriptor, level)
        for descriptor in message_types
    )
    return text
    # return indent(text, " " * level)


def generate_file(
        file_descriptor: FileDescriptorProto
) -> str:
    module = f"{file_descriptor.name[:-len(".proto")]}_pb2"
    qualname = f"{file_descriptor.package}"

    return f"""\
from typing import Mapping, TypedDict, Unpack, overload

from {file_descriptor.package} import {module}

from jetblack_protobuf_gen.serializable import Serializable, MessageMeta


{generate_classes(qualname, module, file_descriptor.message_type, 0)}"""
