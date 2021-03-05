from actions import data, db, write
from datatypes import Line, ResultData
import pandas as pd
import re


def search_line_demo(phone_number: str) -> Line:
    dataset = data.load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_line_all(phone_number))
    return me


def print_columns(data: list[dict], *args) -> None:
    df = pd.DataFrame(data)
    big = pd.DataFrame({s: df[s] for s in args})
    print(big)


if __name__ == '__main__':
    ucdb = db.get_db()
    upper_lines = ucdb.parseall("Phone Number", r'^86465604\d\d', re.I)
    centrex_lines = upper_lines.get_group('Centrex')
    voip_lines = upper_lines.get_group('VoIP')
    print(f'VoIP: {len(voip_lines)}, Centrex: {len(centrex_lines)}')
    