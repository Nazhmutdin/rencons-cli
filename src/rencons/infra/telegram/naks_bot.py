from asyncio import sleep
from re import findall
from typing import AsyncIterator

from httpx import AsyncClient
from telethon import TelegramClient
from telethon.tl.patched import Message

type Kleymo = str
type CertNumber = str
type Link = str
type Page = str


class NaksTelegramBotClient:
    def __init__(
        self, api_id: int, api_hash: str, session: str = "session.session"
    ) -> None:
        self.tg_client = TelegramClient(
            session=session,
            api_id=api_id,
            api_hash=api_hash,
        )
        self.http_client = AsyncClient()

    async def connect(self):
        await self.tg_client.connect()

    async def disconnect(self):
        await self.tg_client.disconnect()

    async def parse_certs_by_kleymo(
        self, kleymo: str
    ) -> list[tuple[Kleymo, CertNumber, Link, Page]]:
        result: list[tuple[str, str, str, str]] = []

        async with self.tg_client.conversation("statnaksbot") as conv:
            msg = await conv.send_message(kleymo)

            response: Message = await conv.get_response(msg)

            amount = 0

            if (
                isinstance(response.message, str)
                and "В реестре зарегистрировано" in response.message
            ):
                amount = int(findall(r"[0-9]+", response.message)[0])

            await sleep(7)

        e = 1

        async for msg in self._iter_messages():
            if e > amount:
                break

            if msg.message is None:
                continue

            if "ПРОВЕРИТЬ ПО ССЫЛКЕ:" in msg.message:
                link = msg.message.split("ПРОВЕРИТЬ ПО ССЫЛКЕ:")[1].strip()
                page = (await self.http_client.get(link)).text

                if "Код не соответствует данным удостоверения" in page:
                    continue

                result.append(
                    (kleymo, msg.message[1:].split("от ")[0].strip(), link, page)
                )

            e += 1

        return result

    async def _iter_messages(self) -> AsyncIterator[Message]:
        async for msg in self.tg_client.iter_messages("statnaksbot"):
            yield msg
