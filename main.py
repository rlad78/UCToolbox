from pathlib import Path
from datatypes import Line
from info import Dataset
from IO import *


def load_dataset() -> Dataset:
    csv_root = Path('/Users/arf/PycharmProjects/VBAReplacer/data_csv')
    file_stack: list[tuple[str, str]] = [
        ('ATT', csv_root / 'ATT.csv'),
        ('COA', csv_root / 'COA.csv'),
        ('HR', csv_root / 'HR.csv'),
        ('MYSOFT', csv_root / 'MySoft.csv'),
        ('SLA', csv_root / 'SLA.csv'),
        ('VOIP', csv_root / 'VoIP.csv'),
        ('BLF', csv_root / 'CXM' / 'BLF.csv'),
        ('BSET', csv_root / 'CXM' / 'BSET.csv'),
        ('CFD', csv_root / 'CXM' / 'CFD.csv'),
        ('CPG', csv_root / 'CXM' / 'CPG.csv'),
        ('LA', csv_root / 'CXM' / 'LA.csv'),
    ]
    fileset = get_file_stack(file_stack)
    return Dataset(fileset)

def search_line(phone_number: str) -> Line:
    dataset = load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_dept_info(phone_number))
    me.update(dataset.get_line_info(phone_number))
    me.update(dataset.get_voip_info(phone_number))
    return me


if __name__ == '__main__':
    print(search_line('8646569969'))
