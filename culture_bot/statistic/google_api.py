from datetime import datetime

from culture_bot.culture_bot import settings


async def spreadsheets_create(wrapper_services):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': settings.SHEET_ID,
                'title': 'Лист',
                'gridProperties': {
                    'rowCount': settings.ROW_COUNT,
                    'columnCount': settings.COLUMN_COUNT
                }
            }
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(wrapper_services, spreadsheetid, email):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
    wrapper_services, some_data, spreadsheetid
):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Общая статистика'],
        [
            'Название маршрута',
            'Количество посетителей',
            'Среднее время',
            'Средняя оценка',
            'Количество отзывов маршрута',
        ]
    ]
    for data in some_data:
        new_row = [
            str(data.name),
            str(data.persons),
            str(data.datetime),
            str(data.rating),
            str(data.review)
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    return await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=settings.RANGE_UPDATE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
