import sys
from time import sleep
from actions import data, db, write
from datatypes import Line, ResultData
import pandas as pd
from fileops import ExcelWriter
from pathlib import Path


if __name__ == '__main__':
    ucdb = db.get_db()
    dataset = ucdb.elevator_lines()._data
    dataset2 = ucdb.fire_lines()._data
    
    fileloc = Path('test.xlsx')
    wb = ExcelWriter(fileloc)
    try:
        # print(wb.write_range(dataset, (1,1)))
        print(wb.write_table(dataset2))
        input()
        same_data = wb.get_table_data()
        print(wb.write_table(same_data))
        # print(wb.write_table(dataset2))
        # input()
        # print(wb.write_table(dataset2))
        # input()
        # print(wb.write_table(dataset2))
        # input()
        # print(wb.write_table(dataset2))
    # except BaseException as e:
    #     print('[[there was an error]] {}'.format(e))
    finally:
        print('press [enter] to finish!')
        input()
        print('closing workbook without saving...')
        wb.close()
        sleep(1)
        print('deleting file...')
        fileloc.unlink()
