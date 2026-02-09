from rencons.core.deps.container import container
from rencons.core.dto import CertDataDTO
from rencons.core.extractors import WelderNaksAttestationPageExtractor
from rencons.infra.telegram.naks_bot import NaksTelegramBotClient


class ParseCertsByKleymoInteractor:
    def __init__(self):
        self.telegram_client = container.get(NaksTelegramBotClient)
        self.extractor = WelderNaksAttestationPageExtractor()

    async def __call__(self, kleymo: str) -> list[CertDataDTO]:
        result: list[CertDataDTO] = []

        await self.telegram_client.connect()

        for el in (await self.telegram_client.parse_certs_by_kleymo(kleymo)):
            result.append(self.extractor(el[3], el[0]))

        return result
