import os
import pandas as pd
import numpy as np


def data_transform():
    # путь до файлов xlsx
    PATH_DIR_FILE_SOURCE: str = os.path.abspath("data/xlsx")

    # получение названий файлов xlsx, кроме name_regions.txt
    SOURCE_FILE_NAMES: list[str] = list(filter(
        lambda file_name: not file_name.__contains__('txt'), os.listdir(PATH_DIR_FILE_SOURCE)))

    # получение названий регионов из файла name_regions.txt
    REGIONS_NAMES: list[str] = get_regions_names(PATH_DIR_FILE_SOURCE)

    # создание словаря с названием регионов и его описанием по годам
    region_result = dict()
    for name in REGIONS_NAMES:
        region_result[name] = pd.DataFrame(
            np.array(range(0, 81)), columns=['Age'])

    # чтение xlsx файла
    for file_name in SOURCE_FILE_NAMES:
        xlsx_file: pd.ExcelFile = pd.ExcelFile(
            f"{PATH_DIR_FILE_SOURCE}\{file_name}")

        # получение названий листов файла
        name_pages: list[str | int] = xlsx_file.sheet_names

        first_i, second_i = get_index_by_name(file_name)

        # чтение листа файла
        for pages in name_pages:
            df: pd.DataFrame = pd.read_excel(xlsx_file, pages)

            # получение имени региона
            name_region = df.values[first_i[0], first_i[1]]
            if name_region in region_result.keys():

                # формирование массива из возраста и числа населения
                year_and_population: list = df.values[second_i[0]:, second_i[1]:second_i[2]].tolist(
                )

                # массив значений до "80 и старше" и "85 и старше"
                year_and_population: list = year_and_population[:get_remove_index(
                    year_and_population) + 1]

                # удаление из массива агрегативных данных
                year_and_population: list = list(filter(lambda v: not (
                    str(v[0]).__contains__('-') or str(v[0]).__contains__('–')), year_and_population))

                # нахождение суммы числа населения за "80 и старше" и "85 и старше"
                summa_last_two_element: int = sum(
                    map(lambda v: v[1], year_and_population[len(year_and_population) - 2:]))

                # получение массива из значений возраста и числа населения без "80 и старше" и "85 и старше"
                year_and_population: list = year_and_population[:len(
                    year_and_population) - 2]

                # добавление суммы в конец списка
                year_and_population.append(['80', summa_last_two_element])

                # добавление года и числа население
                region_result.get(name_region)[f'{file_name[:4]}'] = list(
                    map(lambda v: v[1], year_and_population))

        print(file_name)

    # создание cvs файлов
    for key, df in region_result.items():
        #  регионы, где года идут с 2009 по 2022 включительно
        if df.columns.size == 14:
            df.to_csv(f"data/regions/{key}.csv", sep=';', index=False)


# получение индекста с которого нужно делать срез массива (читать до "85 и старше")
def get_remove_index(array: list) -> int:
    for elem in array:
        if str(elem[0]).__contains__('85'):
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