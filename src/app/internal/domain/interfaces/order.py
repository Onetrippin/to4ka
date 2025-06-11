from abc import ABC, abstractmethod
from typing import Any, Dict, List


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
    def cancel_order(self):
        ...
