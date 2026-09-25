from typing import cast

from google.protobuf.any_pb2 import Any

from protobuf_ex1.pb.envelope_pb2 import EventEnvelope
from protobuf_ex1.pb.events_pb2 import OrderCreated, TradeExecuted

def produce_order() -> bytes:
    order_created = OrderCreated(
        order_id="ORD-123",
        symbol="AAPL",
        quantity=100
    )

    payload = Any()
    payload.Pack(order_created)

    envelope = EventEnvelope(
        event_id="EVT-001",
        source="order-service",
        payload=payload
    )

    return envelope.SerializeToString()

def consume_order(buf: bytes) -> None:
    envelope = cast(EventEnvelope, EventEnvelope.FromString(buf))

    if envelope.payload.Is(OrderCreated.DESCRIPTOR):
        order_created = OrderCreated()
        success = envelope.payload.Unpack(order_created)
        if not success:
            raise ValueError("Failed to unpack OrderCreated")
        print(order_created)
    elif envelope.payload.Is(TradeExecuted.DESCRIPTOR):
        trade_executed = TradeExecuted()
        success = envelope.payload.Unpack(trade_executed)
        if not success:
            raise ValueError("Failed to unpack TradeExecuted")
        print(trade_executed)
    else:
        raise ValueError("Unknown payload")

def main() -> None:
    buf = produce_order()
    consume_order(buf)


if __name__ == "__main__":
    main()

