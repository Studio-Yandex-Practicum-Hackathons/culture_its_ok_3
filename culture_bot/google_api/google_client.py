from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from culture_bot.culture_bot import settings


cred = ServiceAccountCreds(scopes=settings.SCOPES, **settings.INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
