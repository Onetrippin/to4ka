from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Literal
from uuid import UUID

from django.utils import timezone

from app.internal.domain.entities.order import LimitOrderListBody, MarketOrderListBody


class IOrderRepository(ABC):
    @abstractmethod
    def get_order_list(self, user_id: UUID) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_order(self, user_id: UUID, order_id: UUID) -> Dict[str, Any]:
        ...

    @abstractmethod
    def create_limit_order(
        self,
        user_id: UUID,
        order_data: LimitOrderListBody,
        status: str,
        filled: int = 0,
        closed_at: datetime | None = timezone.now(),
    ) -> UUID:
        ...

    @abstractmethod
    def create_market_order(
        self,
        user_id: UUID,
        order_data: MarketOrderListBody,
        status: str,
    ) -> UUID:
        ...

    @abstractmethod
    def execute_market_order(self, trades_info: dict, order_data: MarketOrderListBody) -> UUID:
        ...

    @abstractmethod
    def execute_limit_order(
        self, trades_info: dict, order_data: LimitOrderListBody, status: str = None, filled: int = 0
    ) -> UUID:
        ...

    @abstractmethod
    def create_trades(self, trades_info: dict) -> None:
        ...

    @abstractmethod
    def update_balances(self, trades_info: dict) -> None:
        ...

    @abstractmethod
    def update_order_status(self, trades_info: dict) -> None:
        ...

    @abstractmethod
    def get_opposite_limit_orders_for_market(
        self, direction: Literal['BUY', 'SELL'], ticker: str, user_id: UUID
    ) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_opposite_limit_orders_for_limit(
        self, direction: Literal['BUY', 'SELL'], ticker: str, price: int, user_id: UUID
    ) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def cancel_order(self, user_id: UUID, order_id: UUID) -> None:
        ...

    @abstractmethod
    def get_levels_info(self, ticker: str, limit: int) -> tuple:
        ...

    @abstractmethod
    def get_trans_list(self, ticker: str, limit: int) -> list:
        ...
