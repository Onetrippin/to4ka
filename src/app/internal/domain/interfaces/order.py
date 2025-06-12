from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.internal.common.response_entities import SuccessResponse


class IOrderRepository(ABC):
    @abstractmethod
    def get_order_list(self, user_id: int) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_order(self, user_id: int, order_id: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def create_order(self):
        ...

    @abstractmethod
    def cancel_order(self, user_id: int, order_id: str) -> None:
        ...

    @abstractmethod
    def get_levels_info(self, ticker: str, limit: int) -> tuple:
        ...

    @abstractmethod
    def get_trans_list(self, ticker: str, limit: int) -> list:
        ...