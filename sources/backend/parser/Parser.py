import os

def data_transform():
    PATH_DIR_FILE_SOURCE: str = os.path.abspath("data/xlsx")
    file_name = os.listdir(PATH_DIR_FILE_SOURCE)
    print(file_name)