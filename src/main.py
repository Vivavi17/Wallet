from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import Application
from config import Settings
from controllers.info_controller import InfoController
from controllers.wallets_controller import WalletController
from infra.wallet_repository import WalletRepository
from service.service import WalletService


def create_app():
    settings = Settings()
    engine = create_async_engine(settings.PG_URL)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    repository = WalletRepository(async_session_maker)
    service = WalletService(repository)
    wallet_controller = WalletController(service)
    info_controller = InfoController()

    application = Application([wallet_controller, info_controller]).configure_app()

    return application


app = create_app()
