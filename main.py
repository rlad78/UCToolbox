from pathlib import Path
from datatypes import Line
from info import Dataset
from IO import *
from timeit import default_timer


def load_dataset() -> Dataset:
    print('Loading dataset...', end="")
    start = default_timer()
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
    dataset = Dataset(fileset)
    print(f'loaded! ({(default_timer()-start):.5f}s)')
    return dataset

def search_line(phone_number: str) -> Line:
    dataset = load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_line_all(phone_number))
    return me


if __name__ == '__main__':
    print(search_line('8646569969'))
