from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from culture_bot import settings
from .google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)

cred = ServiceAccountCreds(scopes=settings.SCOPES, **settings.INFO)


async def create_report(data):
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        service = await aiogoogle.discover('sheets', 'v4')
        spreadsheet_id = await spreadsheets_create(service, aiogoogle)
        await set_user_permissions(spreadsheet_id, aiogoogle)
        await spreadsheets_update_value(data, spreadsheet_id, aiogoogle)
        return f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
