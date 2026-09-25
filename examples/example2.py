from jetblack_protobuf_gen.events import OrderCreated, TradeExecuted


def main() -> None:
    order_created = OrderCreated(
        order_id="ORD-001",
        symbol="AAPL",
        quantity=100
    )
    buf = order_created.to_binary()
    roundtrip = OrderCreated.from_binary(buf)
    print(order_created == roundtrip)

    trade_executed = TradeExecuted(
        order_id='ORD-001',
        trade_id="123",
        fills=[
            TradeExecuted.Fill(
                fill_id="FILL-001",
                quantity=10,
                price=23.4
            ),
            TradeExecuted.Fill(
                fill_id="FILL-002",
                quantity=20,
                price=24.1
            ),
        ]
    )

    buf = trade_executed.to_binary()
    roundtrip2 = TradeExecuted.from_binary(buf)
    print(trade_executed == roundtrip2)

    print("here")


if __name__ == "__main__":
    main()
