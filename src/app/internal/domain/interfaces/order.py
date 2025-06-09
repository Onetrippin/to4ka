from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IOrderRepository(ABC):
    @abstractmethod
    def get_order_list(self, user_id: int) -> List[Dict[str, Any]]:
        ...
