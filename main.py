from actions import data, db, write
from datatypes import Line
import pandas as pd


def search_line_demo(phone_number: str) -> Line:
    dataset = data.load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_line_all(phone_number))
    return me


if __name__ == '__main__':
    ucdb = db.get_db()
    print(pd.DataFrame(ucdb.elevator_lines())[['Phone Number', 'Name', 'Room']])
