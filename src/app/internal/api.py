from ninja import NinjaAPI

from app.internal.data.repositories.admin import AdminRepository
from app.internal.data.repositories.order import OrderRepository
from app.internal.data.repositories.user import UserRepository
from app.internal.domain.services.admin import AdminService
from app.internal.domain.services.auth import ApiKeyAuth
from app.internal.domain.services.encryption import EncryptionService
from app.internal.domain.services.order import OrderService
from app.internal.domain.services.user import UserService
from app.internal.presentation.handlers.admin import AdminHandlers
from app.internal.presentation.handlers.order import OrderHandlers
from app.internal.presentation.handlers.user import UserHandlers
from app.internal.presentation.routers.admin import get_admin_routers
from app.internal.presentation.routers.order import get_orders_routers
from app.internal.presentation.routers.user import get_users_router


def get_api():
    api = NinjaAPI(title='To4ka API', version='1.0.0', auth=[ApiKeyAuth()])

    order_repo = OrderRepository()
    order_service = OrderService(order_repo=order_repo)
    order_handlers = OrderHandlers(order_service=order_service)
    order_router = get_orders_routers(order_handlers)
    api.add_router('', order_router)

    user_repo = UserRepository()
    encryption_service = EncryptionService()
    user_service = UserService(user_repo=user_repo, encryption_service=encryption_service)
    user_handlers = UserHandlers(user_service=user_service)
    user_router = get_users_router(user_handlers)
    api.add_router('', user_router)

    admin_repo = AdminRepository()
    admin_service = AdminService(admin_repo=admin_repo)
    admin_handlers = AdminHandlers(admin_service=admin_service)
    admin_router = get_admin_routers(admin_handlers)
    api.add_router('', admin_router)

    return api


ninja_api = get_api()
