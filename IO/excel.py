import pandas as pd


def dicts_to_excel(filename: str, data: list[dict]) -> None:
    pd.DataFrame(data).to_excel(filename)

