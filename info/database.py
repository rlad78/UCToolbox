from datatypes import SourceData, ResultData
from .dataset import Dataset
from pathlib import Path
from fileops import csv_from_dicts
from datatypes import Location, Line
import re


class Database(ResultData):
    def __init__(self, db: list[dict], dataset: Dataset):  # TODO: store dataset within Database class
        super().__init__(db, "Database")
        self.dataset = dataset

    # def query(self, required_matches: dict) -> ResultData:
    #     return ResultData(super(Database, self)._query(required_matches), "Query Data")

    # def parse(self, category: str, regex: str, flags: int) -> dict:
    #     return super(Database, self)._parse(category, regex, flags)

    # def parseall(self, category: str, regex: str, flags: int) -> ResultData:
    #     return ResultData(super(Database, self)._parseall(category, regex, flags), "Parse Data")

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

    def lines(self) -> ResultData:
        return ResultData(self._data, "All Lines")

    def save_db(self, filepath=''):
        if filepath:
            p = Path(filepath)
        else:
            p = Path().cwd() / "ucdb.csv"

        super().to_csv(p.name, p.parent)

        # if "." in p.parts[-1] and p.parent.is_dir():
        #     csv_from_dicts(p, self._data)
        # elif p.is_dir():
        #     csv_from_dicts(p / "ucdb.csv", self._data)

    def fire_lines(self) -> ResultData:
        # fire_name: list[dict] = self.parseall('Name', r'(fire|facp)', re.I)
        # fire_room: list[dict] = self.parseall('Room', r'(fire|alarm|alrm)', re.I)
        # return ResultData(remove_dict_dups(fire_name, fire_room), "Fire Lines")
        return super().get_group("Fire")
        
    def elevator_lines(self) -> ResultData:
        # elev_name: list[dict] = self.parseall('Name', r'(elev|elv)', re.I)
        # elev_room: list[dict] = self.parseall('Room', r'(ele|elv)', re.I)
        # return ResultData(remove_dict_dups(elev_name, elev_room), "Elevator Lines")
        return super().get_group("Elevator")
    
    def emergency_phones(self) -> ResultData:
        # return ResultData(self.parseall("Building", r'(EM\s*PH|EP\s|EP\w{3,4}|EMER.*PHONE)', re.I), "Emergency Phone Lines")
        return super().get_group("Emergency")

    # TODO: build out more searching functionality

def remove_dict_dups(*args) -> list[dict]:
    base_list: list[dict] = [d for lst in args for d in lst]
    base_lines: list[dict] = []
    base_numbers: list[str] = []
    for line in base_list:
        if line['Phone Number'] not in base_numbers:
            base_lines.append(line)
            base_numbers.append(line['Phone Number'])
    return base_lines
