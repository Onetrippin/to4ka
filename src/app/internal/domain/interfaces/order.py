from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from app.internal.common.response_entities import SuccessResponse


class IOrderRepository(ABC):
    @abstractmethod
    def get_order_list(self, user_id: UUID) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_order(self, user_id: UUID, order_id: UUID) -> Dict[str, Any]:
        ...

    @abstractmethod
    def create_order(self):
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
