from datatypes import Line
from info import Dataset, Database
from IO import csv_to_dicts
from pathlib import Path
from tqdm import tqdm
import data


def generate_db(dataset: Dataset) -> Database:
    att_lines = dataset.get_att_numbers()
    db_info: list[dict] = []
    print('Generating UCDB')
    for number in tqdm(att_lines):
        line = Line(number)
        line.update(dataset.get_line_all(number))
        db_info.append(line.info)
    db = Database(db_info)
    db.save_to()
    return db


def read_db(filepath: str) -> Database:
    try:
        csv_data = csv_to_dicts(filepath)
        return Database(csv_data)
    except FileNotFoundError:
        raise Exception(f"[read_db] cannot find {filepath}")


def get_db(dataset=None, database=None):
    if database is None:
        # check if ucdb.csv exists
        p = Path().cwd() / "ucdb.csv"
        if p.is_file():
            database = read_db(str(p))
        # if it doesn't exist, create it from datset
        elif dataset is not None:
            database = generate_db(dataset)
        else:
            database = generate_db(data.load_dataset())
    return database
