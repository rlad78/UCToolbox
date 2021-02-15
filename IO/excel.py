import pandas as pd
import xlsxwriter as xlw


def dicts_to_excel(filename: str, data: list[dict], sheet_name='Sheet1') -> None:
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name=sheet_name)

    worksheet = writer.sheets['Sheet1']
    for i, width in enumerate(__get_col_widths(df)):
        worksheet.set_column(i, i, width)

    cols_to_hide = 7
    total_cols = len(data[0].keys()) + 1
    for n in range(total_cols - cols_to_hide, total_cols):
        worksheet.set_column(n, n, None, None, {'hidden': 1})

    writer.save()


def __get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
