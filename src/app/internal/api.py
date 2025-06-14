from ninja import NinjaAPI

from app.internal.common.auth import ApiKeyAuth
from app.internal.data.repositories.balance import BalanceRepository
from app.internal.data.repositories.instrument import InstrumentRepository
from app.internal.data.repositories.order import OrderRepository
from app.internal.data.repositories.user import UserRepository
from app.internal.domain.services.balance import BalanceService
from app.internal.domain.services.encryption import EncryptionService
from app.internal.domain.services.instrument import InstrumentService
from app.internal.domain.services.order import OrderService
from app.internal.domain.services.user import UserService
from app.internal.presentation.handlers.balance import BalanceHandlers
from app.internal.presentation.handlers.instrument import InstrumentHandlers
from app.internal.presentation.handlers.order import OrderHandlers
from app.internal.presentation.handlers.user import UserHandlers
from app.internal.presentation.routers.balance import get_balance_router
from app.internal.presentation.routers.instrument import get_inst_router
from app.internal.presentation.routers.order import get_orders_routers
from app.internal.presentation.routers.user import get_users_router


def get_api():
    api = NinjaAPI(title='To4ka API', version='1.0.0', auth=[ApiKeyAuth()])

    balance_repo = BalanceRepository()
    balance_service = BalanceService(balance_repo=balance_repo)
    balance_handlers = BalanceHandlers(balance_service=balance_service)
    balance_router = get_balance_router(balance_handlers)
    api.add_router('', balance_router)

    order_repo = OrderRepository()
    order_service = OrderService(order_repo=order_repo, balance_repo=balance_repo)
    order_handlers = OrderHandlers(order_service=order_service)
    order_router = get_orders_routers(order_handlers)
    api.add_router('', order_router)

    user_repo = UserRepository()
    encryption_service = EncryptionService()
    user_service = UserService(user_repo=user_repo, encryption_service=encryption_service)
    user_handlers = UserHandlers(user_service=user_service)
    user_router = get_users_router(user_handlers)
    api.add_router('', user_router)

    inst_repo = InstrumentRepository()
    inst_service = InstrumentService(inst_repo=inst_repo)
    inst_handlers = InstrumentHandlers(inst_service=inst_service)
    inst_router = get_inst_router(inst_handlers)
    api.add_router('', inst_router)

    return api


ninja_api = get_api()
