from enum import IntEnum
from typing import Mapping, TypedDict, Unpack, overload

from jetblack_protobuf_gen.pb import envelope_pb2

from jetblack_protobuf_gen.serializable import Serializable, MessageMeta



class EventEnvelope(
    Serializable[envelope_pb2.EventEnvelope],
    metaclass=MessageMeta,
    message_type=envelope_pb2.EventEnvelope
):


    event_id: str
    source: str
    payload: Serializable

    class Kwargs(TypedDict):
        event_id: str
        source: str
        payload: Serializable


    @overload
    def __init__(
            self,
            instance: envelope_pb2.EventEnvelope,
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

