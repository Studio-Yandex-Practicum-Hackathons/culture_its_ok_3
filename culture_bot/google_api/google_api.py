from datetime import datetime

from culture_bot import settings


async def spreadsheets_create(service, aiogoogle):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'title': 'Общая статистика за все время',
                    'gridProperties': {
                        'rowCount': settings.ROW_COUNT,
                        'columnCount': settings.COLUMN_COUNT
                    }
                }
            }
        ]
    }
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
    now_date_time = datetime.now().strftime(settings.FORMAT)
    service = await aiogoogle.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Общая статистика'],
        [
            'Название маршрута',
            'Количество посетителей',
            'Средняя оценка',
            'Количество отзывов маршрута',
            'Количество комментариев экспонатов'
        ]
    ]
    for key in data.keys():
        new_row = [
            key,
            data[key]['Number_of_visitors'],
            data[key]['Average_rating'],
            data[key]['Number_of_route_reviews'],
            data[key]['Number_of_comments']
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    return await aiogoogle.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=settings.RANGE_UPDATE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
