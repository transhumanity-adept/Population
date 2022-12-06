import os
import pandas as pd


def data_price_transform():

    dict_translete = {
        'январь': "01.01",
        "февраль": "01.02",
        "март": "01.03",
        "апрель": "01.04",
        "май": "01.05",
        "июнь": "01.06",
        "июль": "01.07",
        "август": "01.08",
        "сентябрь": "01.09",
        "октябрь": "01.10",
        "ноябрь": "01.11",
        "декабрь": "01.12"
    }
    PATH_DIR_FILE_SOURCE: str = os.path.abspath("data/PricesRegions")
    FILE_NAME = "Средние цены"
    FILE_PATH = f"{PATH_DIR_FILE_SOURCE}\{FILE_NAME}.xlsx"

    data = pd.read_excel(FILE_PATH)

    string_years = "|".join(
        map(lambda number: str(number), (range(1995, 1998))))

    run_cols = data.columns.str.contains(string_years)

    data.iloc[:, run_cols] = data.iloc[:, run_cols].apply(
        lambda number: round(number / 1000, 2), axis=1)

    colums = ['Product']

    for date in data.columns[1:]:
        split_date = date.split()
        month = split_date[0]
        year = split_date[1]
        if month in dict_translete:
            colums.append(pd.to_datetime(
                f"{dict_translete.get(month)}.{year}"))

    data.columns = colums

    data.to_csv(f"{PATH_DIR_FILE_SOURCE}\{FILE_NAME}.csv", sep=";", index=False)


data_price_transform()
