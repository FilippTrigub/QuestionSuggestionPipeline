import os

import pandas as pd
from pandas import DataFrame

from default_config import all_useful_attributes


def read_kaggle_data() -> DataFrame:
    df = pd.read_csv(os.path.join('data', 'kaggle', 'winemag-data-130k-v2.csv'))
    return df


def read_data_to_df(path: str) -> DataFrame:
    extension = os.path.splitext(path)[1].lower()
    if extension == '.csv':
        return pd.read_csv(path)
    elif extension == '.json':
        return pd.read_json(path)
    else:
        raise ValueError(f'Unsupported file extension: {extension}')


def read_data_to_dict(path: str) -> pd.DataFrame:
    if 'app' in os.listdir() and 'data' not in os.listdir():
        path = os.path.join('app', path)
    return pd.read_json(path)


def reduce_dict_attributes(input_list_of_dicts: list) -> list:
    reduced_dict = []

    for input_list_item in input_list_of_dicts:
        temp_dict = {}
        for attribute in all_useful_attributes:
            if attribute in input_list_item.keys():
                temp_dict[attribute] = input_list_item[attribute]
            else:
                temp_dict[attribute] = {}
        reduced_dict.append(temp_dict)

    return reduced_dict


def reformat_data_for_document_store(input_df: pd.DataFrame) -> list:
    transformed_lst = []
    concat_df = input_df.astype(str).stack().groupby(level=0).apply(', '.join)
    for item in concat_df.to_list():
        transformed_lst.append({'content': item})
    return transformed_lst


def convert_dataframe_to_list_for_document_store(df, columns):
    # Selecting the required columns and converting them to string
    df = df[columns].astype(str)

    # Applying a lambda function to join the columns with ";" and adding "\n" at the end
    result = df.apply(lambda row: ";\n".join(row) + ";\n", axis=1).tolist()

    return result


def convert_dataframe_to_dict(df, text_columns, meta_columns):
    data_dict_list = []

    for index, row in df.iterrows():
        text = ';\n'.join([f'{col}: {row[col]}' for col in text_columns if pd.notnull(row[col])])
        meta = {col: row[col] for col in meta_columns if pd.notnull(row[col])}

        data_dict_list.append({"content": text, "meta": meta})

    return data_dict_list
