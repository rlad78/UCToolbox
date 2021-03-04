from actions import data, db, write
from datatypes import Line
import pandas as pd


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
    print_columns(ucdb.elevator_lines(), 'Phone Number', 'Name', 'Room')
