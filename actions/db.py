from datatypes import Line
from info import Dataset, Database
from fileops import csv_to_dicts
from pathlib import Path
from tqdm import tqdm
from .data import load_dataset


def generate_db(dataset: Dataset) -> Database:
    att_lines = dataset.get_att_numbers()
    db_info: list[dict] = []
    print('Generating UCDB')
    for number in tqdm(att_lines):
        line = Line(number)
        line.update(dataset.get_line_all(number))
        db_info.append(line.info)
    db = Database(db_info, dataset)
    db.save_db()
    return db


def read_db(filepath: str, dataset: Dataset) -> Database:
    try:
        csv_data = csv_to_dicts(filepath)
        return Database(csv_data, dataset)
    except FileNotFoundError:
        raise Exception(f"[read_db] cannot find {filepath}")


def get_db(dataset=None):
    # check if ucdb.csv exists
    p = Path().cwd() / "ucdb.csv"
    if p.is_file() and dataset is None:
        database = read_db(str(p), dataset)
    else:
        database = generate_db(load_dataset())
    return database
