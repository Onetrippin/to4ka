from typing import List
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from app.internal.domain.entities.order import (
    Level,
    LimitOrderListBody,
    LimitOrderListOut,
    MarketOrderListBody,
    MarketOrderListOut,
    OrderBook,
    Transaction,
)
from app.internal.domain.interfaces.balance import IBalanceRepository
from app.internal.domain.interfaces.order import IOrderRepository


class OrderService:
    def __init__(self, order_repo: IOrderRepository, balance_repo: IBalanceRepository) -> None:
        self.order_repo = order_repo
        self.balance_repo = balance_repo

    def _update_status_and_close_if_needed(self, user_id: UUID, order_id: UUID, filled: int) -> None:
        order = self.order_repo.get_order(user_id, order_id)
        status = 'EXECUTED' if filled >= order['quantity'] else 'PARTIALLY_EXECUTED'
        closed_at = timezone.now() if status == 'EXECUTED' else None
        self.order_repo.update_order_status(order_id, status, filled, closed_at)

    def _build_order_out(self, raw_order: dict) -> LimitOrderListOut | MarketOrderListOut:
        if raw_order['type'] == 'limit':
            return LimitOrderListOut(
                id=raw_order['id'],
                status=raw_order['status'].upper(),
                user_id=raw_order['user_id'],
                timestamp=raw_order['created_at'],
                body=LimitOrderListBody(
                    direction=raw_order['direction'].upper(),
                    ticker=raw_order['tool__ticker'],
                    qty=raw_order['quantity'],
                    price=raw_order['price'],
                ),
                filled=raw_order['filled'],
            )

        return MarketOrderListOut(
            id=raw_order['id'],
            status=raw_order['status'].upper(),
            user_id=raw_order['user_id'],
            timestamp=raw_order['created_at'],
            body=MarketOrderListBody(
                direction=raw_order['direction'].upper(),
                ticker=raw_order['tool__ticker'],
                qty=raw_order['quantity'],
            ),
        )

    def get_order_list(self, user_id: UUID) -> List[LimitOrderListOut | MarketOrderListOut]:
        raw_orders = self.order_repo.get_order_list(user_id)

        return [self._build_order_out(raw_order) for raw_order in raw_orders]

    def get_order(self, user_id: UUID, order_id: UUID) -> LimitOrderListOut | MarketOrderListOut:
        raw_order = self.order_repo.get_order(user_id, order_id)

        return self._build_order_out(raw_order)

    def cancel_order(self, user_id: UUID, order_id: UUID) -> None:
        return self.order_repo.cancel_order(user_id, order_id)

    def get_orderbook(self, ticker: str, limit: int) -> OrderBook:
        bids, asks = self.order_repo.get_levels_info(ticker, limit)
        return OrderBook(
            bid_levels=[Level(price=bid['price'], qty=bid['quantity']) for bid in bids],
            ask_levels=[Level(price=ask['price'], qty=ask['quantity']) for ask in asks],
        )

    def get_trans_history(self, ticker: str, limit: int) -> list[Transaction]:
        return [
            Transaction(
                ticker=trans['tool__ticker'], amount=trans['quantity'], price=trans['price'], timestamp=trans['date']
            )
            for trans in self.order_repo.get_trans_list(ticker, limit)
        ]

    def create_market_order(self, user_id: UUID, order_data: MarketOrderListBody) -> UUID:
        opposite_orders = self.order_repo.get_opposite_limit_orders_for_market(order_data.direction, order_data.ticker)
        if sum([opp['quantity'] for opp in opposite_orders]) < order_data.qty:
            order = self.order_repo.create_market_order(
                user_id=user_id,
                order_data=order_data,
                status='CANCELLED',
            )
        else:
            total_price = 0
            remaining_qty = order_data.qty
            trades_info = {
                'user_id': user_id,
                'direction': order_data.direction,
                'trades': []
            }
            for opp in opposite_orders:
                available_qty = opp['quantity'] - opp['filled']
                trade_qty = min(remaining_qty, available_qty)
                trades_info['trades'].append({
                    'match_order_id': opp['id'],
                    'tool_id': opp['tool_id'],
                    'user_id': opp['user_id'],
                    'price': opp['price'],
                    'quantity': trade_qty,
                })
                total_price += trade_qty * opp['price']
                remaining_qty -= trade_qty
                if remaining_qty <= 0:
                    break
            if order_data.direction == 'BUY' and self.balance_repo.get_balance_by_ticker(user_id) < total_price:
                order = self.order_repo.create_market_order(
                    user_id=user_id,
                    order_data=order_data,
                    status='CANCELLED',
                )
            else:




        return order.id

        order = self.order_repo.create_market_order(
            user_id=user_id,
            order_data=order_data,
            status='EXECUTED',
            filled=total_filled,
            closed_at=timezone.now(),
        )
        return order.id

    def create_limit_order(self, user_id: UUID, order_data: LimitOrderListBody) -> UUID:
        ...
