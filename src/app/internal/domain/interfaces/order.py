from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Literal
from uuid import UUID

from app.internal.data.models.order import Order
from app.internal.data.models.trade import Trade
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
            closed_at: Optional[datetime] = None,
    ) -> Order:
        ...

    @abstractmethod
    def create_market_order(
            self,
            user_id: UUID,
            order_data: MarketOrderListBody,
            status: str,
    ) -> Order:
        ...

    @abstractmethod
    def execute_market_order(self, trades_info: dict) -> None:
        ...

    @abstractmethod
    def create_trade_from_match(
            self,
            user_id: UUID,
            direction: Literal["BUY", "SELL"],
            match_order_id: UUID,
            tool_id: UUID,
            price: float,
            quantity: int,
    ) -> Trade:
        ...

    @abstractmethod
    def update_order_status(self, order_id: UUID, status: str, filled: Optional[int], closed_at: Optional[datetime]):
        ...

    @abstractmethod
    def get_opposite_limit_orders_for_market(self, direction: Literal['BUY', 'SELL'], ticker: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_opposite_limit_orders_for_limit(self, direction: Literal['BUY', 'SELL'], ticker: str, price: float) -> List[Dict[str, Any]]:
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
