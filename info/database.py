from datatypes.sourcedata import SourceData
from .dataset import Dataset
from pathlib import Path
from fileops import csv_from_dicts
from datatypes import Location, Line
import re


class Database(SourceData):
    def __init__(self, db: list[dict], dataset: Dataset):  # TODO: store dataset within Database class
        super(Database, self).__init__(db)
        self.dataset = dataset

    def query(self, required_matches: dict) -> list[dict]:
        return super(Database, self)._query(required_matches)

    def parse(self, category: str, regex: str, flags: int) -> dict:
        return super(Database, self)._parse(category, regex, flags)

    def parseall(self, category: str, regex: str, flags: int) -> list[dict]:
        return super(Database, self)._parseall(category, regex, flags)

    def lines_by_building(self) -> dict[str, Location]:
        """
        dict: sla, Location
        """
        by_buildings: dict[str, Location] = {}
        for entry in self._data:
            sla = entry["sla_nbr"]
            if sla not in by_buildings.keys():
                location_info = self.dataset.get_location_info(sla_num=sla)
                if not location_info:
                    this_location = Location({'SLA': sla, 'Name': 'SLA ' + str(sla)})
                this_location = Location(location_info)
                this_location.add_line(Line(entry['Phone Number'], entry))
                by_buildings[sla] = this_location
            else:
                by_buildings[sla].add_line(Line(entry['Phone Number'], entry))
        return by_buildings

    def centrex_by_building(self) -> dict[str, Location]:
        buildings: dict[str, Location] = dict()
        for entry in self._data:
            if entry['line_type'] == 'VOIP':
                continue
            sla = entry['sla_nbr']
            if sla not in buildings.keys():
                bldg_info = self.dataset.get_location_info(sla_num=sla)
                if not bldg_info:
                    building = Location({'SLA': sla, 'Name': 'SLA ' + sla})
                else:
                    building = Location(bldg_info)
                building.add_line(Line(entry['Phone Number'], entry))
                buildings[sla] = building
            else:
                buildings[sla].add_line(Line(entry['Phone Number'], entry))
        return buildings

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
