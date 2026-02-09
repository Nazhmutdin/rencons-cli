from dishka import Provider, Scope, make_container, provide

from rencons.config import CliConfig
from rencons.infra.telegram.naks_bot import NaksTelegramBotClient


class MainProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_naks_telegram_bot_client(self) -> NaksTelegramBotClient:
        return NaksTelegramBotClient(
            CliConfig.API_ID(),
            CliConfig.API_HASH(),
        )


container = make_container(MainProvider())
