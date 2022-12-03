import os
import pandas as pd
import numpy as np
from collections import namedtuple


def data_transform():
    PATH_DIR_FILE_SOURCE: str = os.path.abspath("data/xlsx")
    SOURCE_FILE_NAMES: list[str] = list(filter(
        lambda file_name: not file_name.__contains__('txt'), os.listdir(PATH_DIR_FILE_SOURCE)))
    REGIONS_NAMES: list[str] = get_regions_names(PATH_DIR_FILE_SOURCE)


    df_result:pd.DataFrame = pd.DataFrame(np.array(range(0, 81)), columns=['Age'])

    for file_name in SOURCE_FILE_NAMES:
        xlsx_file: pd.ExcelFile = pd.ExcelFile(
            f"{PATH_DIR_FILE_SOURCE}\{file_name}")
        name_pages: list[str | int] = xlsx_file.sheet_names


        for pages in name_pages:
            df: pd.DataFrame = pd.read_excel(xlsx_file, pages)

            first_i, second_i = get_index_by_name(file_name)

            if df.values[first_i[0], first_i[1]] == "Белгородская область":
                year_and_population: list = df.values[second_i[0]:, second_i[1]:second_i[2]].tolist()

                year_and_population: list = year_and_population[:get_remove_index(
                    year_and_population) + 1]
                year_and_population: list = list(filter(lambda v: not (
                    v[0].__contains__('-') or v[0].__contains__('–')), year_and_population))

                summa_last_two_element: int = sum(
                    map(lambda v: v[1], year_and_population[len(year_and_population) - 2:]))
                year_and_population: list = year_and_population[:len(
                    year_and_population) - 2]
                year_and_population.append(['80', summa_last_two_element])

                df_result[f'{file_name[:4]}'] = list(map(lambda v: v[1], year_and_population))
        print(file_name)
    
    df_result.to_csv(f"data/regions/Белгород.csv", sep=';')

     


def get_remove_index(array: list) -> int:
    for elem in array:
        if elem[0].__contains__('85'):
            return array.index(elem)


def get_regions_names(path: str) -> list[str]:
    with open(f"{path}/name_regions.txt") as f:
        read = [string.replace("\n", "") for string in f.readlines()]
    return read


def get_index_by_name(file_name: str):
    match file_name:
        case '2021.xlsx' | '2022.xlsx':
            return ([0, 0], [5, 0, 2])
        case _:
            return ([2, 1], [8, 1, 3])


data_transform()
# df_result:pd.DataFrame = pd.DataFrame(np.array(range(0, 81)), columns=['Age'])
# print(df_result)
# x = '2022.xlsx'
# print(x[:4])

