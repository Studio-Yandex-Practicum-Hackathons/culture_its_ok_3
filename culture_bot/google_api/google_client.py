from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from culture_bot import settings

from .google_api import (set_user_permissions, spreadsheets_create,
                         spreadsheets_update_value)

cred = ServiceAccountCreds(scopes=settings.SCOPES, **settings.INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle


async def create_general_report(data):
    async for aiogoogle in get_service():
        spreadsheet_id = await spreadsheets_create(aiogoogle, data)
        await set_user_permissions(spreadsheet_id, aiogoogle)
        await spreadsheets_update_value(data, spreadsheet_id, aiogoogle)
        return f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
