import os
import pandas as pd


def data_transform():
    PATH_DIR_FILE_SOURCE: str = os.path.abspath("data/xlsx")
    SOURCE_FILE_NAMES: list[str] = list(filter(lambda file_name: not file_name.__contains__('txt'), os.listdir(PATH_DIR_FILE_SOURCE)))
    REGIONS_NAMES: list[str] = get_regions_names(PATH_DIR_FILE_SOURCE) 

    stoper = 0
    
    for file_name in SOURCE_FILE_NAMES:
        xlsx_file: pd.ExcelFile = pd.ExcelFile(f"{PATH_DIR_FILE_SOURCE}\{file_name}")
        name_pages: list[str|int] = xlsx_file.sheet_names
        
        for pages in name_pages:
            df = pd.read_excel(xlsx_file, pages)
            print(df)

            

        if stoper == 0:
                break





        


def get_regions_names(path: str) -> list[str]:
    with open(f"{path}/name_regions.txt") as f:
        read = [string.replace("\n", "") for string in f.readlines()]
    return read


data_transform()


