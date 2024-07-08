import os
import pandas as pd
import re
from unidecode import unidecode
import config


def find_all_files():
    upload_files = os.listdir('upload')
    for file in upload_files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            abas = config.abas.get(file)
            if abas:
                for aba in abas:
                    convert_csv(file, aba)
            else:
                convert_csv(file)


def convert_csv(file, aba=None):
    read_file = pd.read_excel(f'upload/{file}', aba)
    read_file = list(read_file.items())[0][1] if aba is None else read_file

    # Remove duplicate rows (keep the last occurrence)
    read_file = read_file.loc[~read_file.duplicated(keep='last')]

    # Replace newlines and carriage returns with spaces
    read_file = read_file.replace('\n', ' ', regex=True).replace('\r', '', regex=True)

    # Convert column names to snake_case and remove leading/trailing whitespaces
    new_columns = [snake_small_case(column.strip()) for column in read_file.columns]
    read_file.columns = new_columns

    for column in new_columns:
        # Remove leading/trailing whitespaces from each cell value
        read_file[column] = [value.strip() if isinstance(value, str) else value for value in read_file[column]]

    # Save to CSV with append mode (but overwrite existing rows with duplicates)
    read_file.to_csv(f'dataset/data/{file.split(".xls")[0]}.csv' if aba is None else f'dataset/data/{aba}.csv',
                     index=False, header=True, sep=',', decimal=',', encoding='utf-8-sig', na_rep="", mode='w')  # Change mode to 'w' to overwrite duplicates


def snake_small_case(column):
    column_lower = column.lower()
    column_unidecode = unidecode(column_lower)
    column_alphanumeric = re.sub('[^A-Za-z0-9]+', ' ', column_unidecode)
    column_split = column_alphanumeric.split(' ')
    column_empty = [x for x in column_split if x != '']
    column = '_'.join(column_empty)
    return column


if __name__ == '__main__':
    find_all_files()

