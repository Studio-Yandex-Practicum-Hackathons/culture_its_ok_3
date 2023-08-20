from culture_bot import settings
from .utils import create_spreadsheet_body, create_table_values


async def spreadsheets_create(aiogoogle, data):
    service = await aiogoogle.discover('sheets', 'v4')
    spreadsheet_body = await create_spreadsheet_body(data)
    response = await aiogoogle.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(spreadsheet_id, aiogoogle):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.EMAIL
    }
    service = await aiogoogle.discover('drive', 'v3')
    await aiogoogle.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
    data, spreadsheetid, aiogoogle
):
    service = await aiogoogle.discover('sheets', 'v4')
    
    sheet_names = {
        'for_general_report': 'Общая статистика за все время',
        'for_days_report': 'Статистика по дням',
        'for_routes_report': [data['for_routes_report'].keys()]
    }
    for name in sheet_names.keys():
        if name in data.keys() and name != 'for_routes_report':
            table_values = await create_table_values(data, name)
            update_body = {
                'majorDimension': 'ROWS',
                'values': table_values
            }
            
            range_name = f"{sheet_names[name]}!A1"
            await aiogoogle.as_service_account(
                service.spreadsheets.values.update(
                    spreadsheetId=spreadsheetid,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    json=update_body
                )
            )
        if name in data.keys() and name == 'for_routes_report':
            for name_route, _ in data['for_routes_report'].items():
                table_values = await create_table_values(
                    data, name, name_route=name_route
                )
                update_body = {
                    'majorDimension': 'ROWS',
                    'values': table_values
                }
                range_name = f"{name_route}!A1"
                await aiogoogle.as_service_account(
                    service.spreadsheets.values.update(
                        spreadsheetId=spreadsheetid,
                        range=range_name,
                        valueInputOption='USER_ENTERED',
                        json=update_body
                    )
                )
