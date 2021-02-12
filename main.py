from pathlib import Path
from datatypes import Line
from info import Dataset
from IO import *
from timeit import default_timer
from tqdm import tqdm


def load_dataset() -> Dataset:
    print('Loading dataset...', end="")
    start = default_timer()
    # csv_root = Path('/Users/arf/PycharmProjects/VBAReplacer/data_csv')
    csv_root = Path('C:/Users/gooby/PycharmProjects/VBAReplacer/data_csv')
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
    fileset = csv_file_stack(file_stack)
    dataset = Dataset(fileset)
    print(f'loaded! ({(default_timer() - start):.5f}s)')
    return dataset


def generate_db(dataset: Dataset) -> list[dict]:
    att_lines = dataset.get_att_numbers()
    db: list[dict] = []
    print('Generating UCDB')
    for number in tqdm(att_lines):
        line = Line(number)
        line.update(dataset.get_line_all(number))
        db.append(line.info)
    return db


def search_line_demo(phone_number: str) -> Line:
    dataset = load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_line_all(phone_number))
    return me


if __name__ == '__main__':
    # csv_from_dicts('ucdb.csv', generate_db(load_dataset()))
    print(search_line_demo(input('Phone number: ')))
