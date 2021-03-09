from actions import data, db, write
from datatypes import Line, ResultData
import pandas as pd
import re


if __name__ == '__main__':
    ucdb = db.get_db()
    emg_lines = ucdb.emergency_phones()
    print(emg_lines)
