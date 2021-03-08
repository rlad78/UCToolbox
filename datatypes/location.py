from .line import Line
from .sourcedata import Entry
from fileops import dicts_to_excel
from pathlib import Path
from pathvalidate import sanitize_filename, sanitize_filepath
import re


class Location(Entry):
    def __init__(self, building_data: dict):
        super(Location, self).__init__(building_data)
        self.building = building_data.get('Name', "").replace(" / ", " ").replace("/", "")
        self.address = building_data.get('Address', "")
        self.sla = building_data.get('SLA', "")
        self.bldg_id = building_data.get('Building ID', "")
        self.lines: list[Line] = []

    def __str__(self):
        out: str = f'{self.building} (SLA {self.sla})  BLDG IDs: [{self.bldg_id}]\n'
        out += self.address
        return out

    def append_bldg_id(self, bldg_id: str) -> None:
        bldg_id_parts = self.bldg_id.split(', ')
        if bldg_id not in bldg_id_parts:
            self.bldg_id = ", ".join(bldg_id_parts + [bldg_id])

    def add_line(self, line: Line) -> None:
        if line is None:
            return None
        if line['sla_nbr'] == self.sla:
            self.lines.append(line)

    def lines_dict(self, lines=None) -> list[dict]:
        if lines is None:
            lines = self.lines
        # return [{k: v} for n in lines for k, v in n.info.items()]
        line_list: list[dict] = []
        for line in lines:
            line_list.append(line.info)
        return line_list

    def pull_lines_by_fiman(self) -> dict[str, list[dict]]:
        fiman_groups: dict[str, list[Line]] = dict()

        # make a separate fiman group for blank/unassigned lines
        fiman_groups['UNASSIGNED'] = []
        for line in self.lines:
            fiman = line['Financial Manager']
            if line['line_type'] == 'VOIP':
                continue
            elif not fiman:
                fiman_groups['UNASSIGNED'].append(line)
            elif fiman not in fiman_groups.keys():
                fiman_groups[fiman] = [line]  # if the fiman group hasn't been made yet, make it with a new list
            else:
                fiman_groups[fiman].append(line)

        # # remove blanks and convert Line objects to dict lists
        return {fi: self.lines_dict(lns) for fi, lns in fiman_groups.items() if lns}

    def pull_ems_lines(self) -> list[dict]:
        s_ems = re.compile(r'(elev|elv|fire|facp)', re.IGNORECASE)

        # get all lines that have ems keywords in their names or rooms
        ems_lines: list[Line] = [line for line in self.lines if
                                 re.search(s_ems, line['Name']) or re.search(s_ems, line['Room'])]

        return self.lines_dict(ems_lines) if ems_lines else []

    def is_emergency_location(self) -> bool:
        if re.search(r'(EM\s*PH|EP\s|EP\w{3,4}|EMER.*PHONE)', self.building):
            return True
        else:
            return False

    def summary(self) -> dict:
        info: dict = {
            "Building": self.building,
            "Line Count": len(self.lines),
            "Elevator(s)?": "",
            "EMPH": False
        }
        if re.search(r'(EM\s*PH|EP\s|EP\w{3,4}|EMER.*PHONE)', self.building):
            info['EMPH'] = True

        elev_check: bool = False
        s_elv = re.compile(r'(elev|elv)', re.IGNORECASE)
        for line in self.lines:
            if re.search(s_elv, line['Name']) or re.search(s_elv, line['Room']):
                elev_check = True
        if elev_check:
            info['Elevator(s)?'] = "YES"

        return info
