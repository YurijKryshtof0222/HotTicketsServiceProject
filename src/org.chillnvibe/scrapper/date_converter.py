import re
from datetime import datetime, timedelta

pattern = r'(\d+)\s*([^\d\s]+)\s*-\s*(\d+)\s*([^\d\s]+)'


def convert_do_date(trip_duration_str):
    match = re.match(pattern, trip_duration_str)

    if match:
        start_day, start_month, end_day, end_month = match.groups()

        # Визначення словника для мапінгу назв місяців на їх числові еквіваленти
        month_dict = {
            'січ': 1, 'лют': 2, 'бер': 3, 'кві': 4, 'тра': 5, 'чер': 6,
            'лип': 7, 'сер': 8, 'вер': 9, 'жов': 10, 'лис': 11, 'гру': 12
        }

        # Конвертація назв місяців у числа
        start_month_num = month_dict.get(start_month.lower())
        end_month_num = month_dict.get(end_month.lower())

        if start_month_num is not None and end_month_num is not None:
            # Створення дат на основі чисел та місяців
            start_date = datetime(datetime.now().year, start_month_num, int(start_day))
            end_date = datetime(datetime.now().year, end_month_num, int(end_day))

        # Виведення результату
        #     print("Початкова дата:", start_date.strftime("%d.%m.%Y"))
        #     print("Кінцева дата:", end_date.strftime("%d.%m.%Y"))
            return start_date, end_date
    raise Exception("Couldn't format this trip duration")