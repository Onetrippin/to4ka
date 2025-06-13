from typing import List
from uuid import UUID

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

    def cancel_order(self, user_id: UUID, order_id: UUID) -> bool:
        return self.order_repo.cancel_order(user_id, order_id)

    def get_orderbook(self, ticker: str, limit: int) -> OrderBook:
        bids, asks = self.order_repo.get_levels_info(ticker, limit)
        return OrderBook(
            bid_levels=[Level(price=bid['price'], qty=bid['quantity'] - bid['filled']) for bid in bids],
            ask_levels=[Level(price=ask['price'], qty=ask['quantity'] - ask['filled']) for ask in asks],
        )

    def get_trans_history(self, ticker: str, limit: int) -> list[Transaction]:
        return [
            Transaction(
                ticker=trans['tool__ticker'], amount=trans['quantity'], price=trans['price'], timestamp=trans['date']
            )
            for trans in self.order_repo.get_trans_list(ticker, limit)
        ]

    def create_market_order(self, user_id: UUID, order_data: MarketOrderListBody) -> tuple[UUID | None, str]:
        opposite_orders = self.order_repo.get_opposite_limit_orders_for_market(
            order_data.direction,
            order_data.ticker,
            user_id,
        )
        if sum([opp['quantity'] for opp in opposite_orders]) < order_data.qty:
            self.order_repo.create_market_order(
                user_id=user_id,
                order_data=order_data,
                status='CANCELLED',
            )
            text = f'1) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}'
            return None, text
        else:
            total_price = 0
            remaining_qty = order_data.qty
            trades_info = {'user_id': user_id, 'direction': order_data.direction, 'trades': []}
            for opp in opposite_orders:
                available_qty = opp['quantity'] - opp['filled']
                trade_qty = min(remaining_qty, available_qty)
                trades_info['trades'].append(
                    {
                        'match_order_id': opp['id'],
                        'tool_id': opp['tool_id'],
                        'user_id': opp['user_id'],
                        'price': opp['price'],
                        'quantity': trade_qty,
                        'init_quantity': opp['quantity'],
                        'init_filled': opp['filled'],
                    }
                )
                total_price += trade_qty * opp['price']
                remaining_qty -= trade_qty
                if remaining_qty <= 0:
                    break
            if (
                order_data.direction == 'BUY'
                and (not total_price or self.balance_repo.get_balance_by_ticker(user_id) < total_price)
                or order_data.direction == 'SELL'
                and self.balance_repo.get_balance_by_ticker(user_id, order_data.ticker) < order_data.qty
            ):
                self.order_repo.create_market_order(
                    user_id=user_id,
                    order_data=order_data,
                    status='CANCELLED',
                )
                text = (
                    f'2) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}, '
                    f'total_price: {total_price}, remaining_qty: {remaining_qty}'
                    f'balance: {self.balance_repo.get_balance_by_ticker(user_id) if order_data.direction == 'BUY' else
                    self.balance_repo.get_balance_by_ticker(user_id, order_data.ticker)}'
                )
                return None, text
            text = (
                f'3) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}, '
                f'total_price: {total_price}, remaining_qty: {remaining_qty}'
            )
            return self.order_repo.execute_market_order(trades_info, order_data), text

    def create_limit_order(self, user_id: UUID, order_data: LimitOrderListBody) -> tuple[UUID | None, str]:
        opposite_orders = self.order_repo.get_opposite_limit_orders_for_limit(
            order_data.direction, order_data.ticker, order_data.price, user_id
        )
        total_price = 0
        remaining_qty = order_data.qty
        trades_info = {'user_id': user_id, 'direction': order_data.direction, 'trades': []}
        for opp in opposite_orders:
            available_qty = opp['quantity'] - opp['filled']
            trade_qty = min(remaining_qty, available_qty)
            trades_info['trades'].append(
                {
                    'match_order_id': opp['id'],
                    'tool_id': opp['tool_id'],
                    'user_id': opp['user_id'],
                    'price': opp['price'],
                    'quantity': trade_qty,
                    'init_quantity': opp['quantity'],
                    'init_filled': opp['filled'],
                }
            )
            total_price += trade_qty * opp['price']
            remaining_qty -= trade_qty
            if remaining_qty <= 0:
                break

        if (
            order_data.direction == 'BUY'
            and (not total_price or self.balance_repo.get_balance_by_ticker(user_id) < total_price)
            or order_data.direction == 'SELL'
            and self.balance_repo.get_balance_by_ticker(user_id, order_data.ticker) < order_data.qty
        ):
            self.order_repo.create_limit_order(
                user_id=user_id,
                order_data=order_data,
                status='CANCELLED',
            )
            text = (
                f'4) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}, '
                f'total_price: {total_price}, remaining_qty: {remaining_qty} '
                f'balance: {self.balance_repo.get_balance_by_ticker(user_id) if order_data.direction == 'BUY' else
                self.balance_repo.get_balance_by_ticker(user_id, order_data.ticker)}'
            )
            return None, text
        elif remaining_qty == order_data.qty:
            text = (
                f'5) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}, '
                f'total_price: {total_price}, remaining_qty: {remaining_qty}'
            )
            order_id = self.order_repo.execute_limit_order(trades_info, order_data)
        elif remaining_qty <= 0:
            text = (
                f'6) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}, '
                f'total_price: {total_price}, remaining_qty: {remaining_qty}'
            )
            order_id = self.order_repo.execute_limit_order(
                trades_info, order_data, 'EXECUTED', order_data.qty - remaining_qty
            )
        else:
            text = (
                f'7) opposites: {opposite_orders}, user_id: {user_id}, order_data: {order_data}, '
                f'total_price: {total_price}, remaining_qty: {remaining_qty}'
            )
            order_id = self.order_repo.execute_limit_order(
                trades_info, order_data, 'PARTIALLY_EXECUTED', order_data.qty
            )
        return order_id, text
