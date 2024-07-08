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

    # Identify potential date columns (assuming YYYY-MM-DD format)
    potential_date_cols = [col for col in new_columns if re.match(r'\d{4}-\d{2}-\d{2}$', read_file[col].head(1).values[0])]

    # Convert potential date columns to date type (excluding time)
    for col in potential_date_cols:
        try:
            read_file[col] = pd.to_datetime(read_file[col], format='%Y-%m-%d').dt.date
        except (ValueError, AttributeError):
            # Handle cases where conversion fails (e.g., non-convertible formats)
            pass

    for column in new_columns:
        # Remove leading/trailing whitespaces from each cell value
        read_file[column] = [value.strip() if isinstance(value, str) else value for value in read_file[column]]

    # Read existing data (if any)
    try:
        existing_data = pd.read_csv(f'dataset/data/{file.split(".xls")[0]}.csv' if aba is None else f'dataset/data/{aba}.csv')
    except FileNotFoundError:
        existing_data = pd.DataFrame()  # Create empty DataFrame if file doesn't exist

    # Combine existing and new data, removing duplicates (keep last occurrence)
    combined_data = pd.concat([existing_data, read_file], ignore_index=True).drop_duplicates(keep='last')

    # Save combined data to CSV
    combined_data.to_csv(f'dataset/data/{file.split(".xls")[0]}.csv' if aba is None else f'dataset/data/{aba}.csv',
                         index=False, header=True, sep=',', decimal=',', encoding='utf-8-sig', na_rep="")


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



