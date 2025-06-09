from ninja import NinjaAPI

from app.internal.data.repositories.order import OrderRepository
from app.internal.domain.services.order import OrderService
from app.internal.presentation.handlers.order import OrderHandlers
from app.internal.presentation.routers.order import get_orders_routers


def get_api():
    api = NinjaAPI(title='To4ka API', version='1.0.0')

    # api.add_router({path}, {router})
    order_repo = OrderRepository()
    order_service = OrderService(order_repo=order_repo)
    order_handlers = OrderHandlers(order_service=order_service)
    order_router = get_orders_routers(order_handlers)
    api.add_router('', order_router)

    return api


ninja_api = get_api()
