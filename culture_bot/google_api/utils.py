from datetime import datetime

from culture_bot import settings


async def create_spreadsheet_body(data):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    grid_properties = {
        'rowCount': settings.ROW_COUNT,
        'columnCount': settings.COLUMN_COUNT
    }
    
    route_sheets = [
        {
            'properties': {'title': title, 'gridProperties': grid_properties}
        } for title in data['for_routes_report']
    ]
    exhibit_sheets = [
        {
            'properties': {'title': title, 'gridProperties': grid_properties}
        } for title in data['for_exhibits_report']
    ]
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'title': 'Общая статистика за все время',
                    'gridProperties': grid_properties
                }
            },
            {
                'properties': {
                    'title': 'Статистика по дням',
                    'gridProperties': grid_properties
                }
            },
            *route_sheets,
            *exhibit_sheets
        ]
    }
    return spreadsheet_body


async def create_table_values(data, name, name_obj=None):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    if name == 'for_general_report':
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
        data_general = data['for_general_report']
        for key in data_general.keys():
            new_row = [
                key,
                data_general[key]['Number_of_visitors'],
                data_general[key]['Average_rating'],
                data_general[key]['Number_of_route_reviews'],
                data_general[key]['Number_of_comments']
            ]
            table_values.append(new_row)
        return table_values
    if name == 'for_days_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Статистика по дням'],
            [
                'День',
                'Количество посетителей',
                'Количество отзывов',
                'Количество комментариев',
            ]
        ]
        data_days = data['for_days_report']
        for key in data_days.keys():
            new_row = [
                key,
                data_days[key]['visitors'],
                data_days[key]['reviews'],
                data_days[key]['comments'],
            ]
            table_values.append(new_row)
        return table_values
    if name == 'for_routes_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Статистика по дням'],
            [
                'Маршрут',
                'Дата и время',
                'Рейтинг',
                'Телеграм id',
                'Отзыв'
            ]
        ]
        data_route = data['for_routes_report'][name_obj]
        for data_value in data_route:
            new_row = [
                name_obj,
                data_value['Data'],
                data_value['Rating'],
                data_value['Telegram_ID'],
                data_value['Review'],
            ]
            table_values.append(new_row)
        return table_values
    if name == 'for_exhibits_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Статистика по дням'],
            [
                'Экспонат',
                'Маршрут',
                'Дата и время',
                'Рейтинг',
                'Телеграм id',
                'Комментарий'
            ]
        ]
        data_exhibit = data['for_exhibits_report'][name_obj]
        for data_value in data_exhibit:
            new_row = [
                name_obj,
                data_value['Name_route'],
                data_value['Data'],
                data_value['Rating'],
                data_value['Telegram_ID'],
                data_value['Comment'],
            ]
            table_values.append(new_row)
        return table_values
