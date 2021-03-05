from actions import data, db, write
from datatypes import Line, ResultData
import pandas as pd
import re


if __name__ == '__main__':
    ucdb = db.get_db()
    upper_lines = ucdb.parseall("Phone Number", r'^86465604\d\d', re.I)
    less_lines = upper_lines.parse("Phone Number", r'864656041\d')
    line_types: dict[str, ResultData] = less_lines.group_by('Financial Manager')
    print(line_types.keys())
