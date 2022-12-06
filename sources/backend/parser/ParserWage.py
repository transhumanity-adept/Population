import os
import pandas as pd

def data_price_transform():
    PATH_DIR_FILE_SOURCE: str = os.path.abspath("data/PricesRegions")
    FILE_NAME = "Средняя заработная плата"
    FILE_PATH = f"{PATH_DIR_FILE_SOURCE}\{FILE_NAME}.xlsx"

    data = pd.read_excel(FILE_PATH)

    date = []
    date.append('Region')
    for time in pd.to_datetime({'year': data.columns[1:],
                                'month': [1 for i in range(0, len(data.columns) - 1)],
                                'day': [1 for i in range(0, len(data.columns) - 1)]}):
        date.append(time)

    data.columns = date

    data.to_csv(f"{PATH_DIR_FILE_SOURCE}\{FILE_NAME}.csv", sep=";", index=False)


data_price_transform()
