from .formats import SourceData
from .dataset import Dataset
from pathlib import Path
from IO import csv_from_dicts
from datatypes import Location, Line


class Database(SourceData):
    def __init__(self, db: list[dict]):  # TODO: store dataset within Database class
        super(Database, self).__init__(db)

    def query(self, required_matches: dict):
        super(Database, self)._query(required_matches)

    def lines_by_building(self) -> dict[str, Location]:
        """
        dict: sla, Location
        """
        by_buildings: dict[str, Location] = {}
        for line in self._data:
            sla = line["sla_nbr"]
            if sla not in by_buildings.keys():



    def lines(self) -> list[dict]:
        return self._data

    def save_to(self, filepath=''):
        if filepath:
            p = Path(filepath)
        else:
            p = Path().cwd() / "ucdb.csv"

        if "." in p.parts[-1] and p.parent.is_dir():
            csv_from_dicts(p, self._data)
        elif p.is_dir():
            csv_from_dicts(p / "ucdb.csv", self._data)

    # TODO: build out more searching functionality
