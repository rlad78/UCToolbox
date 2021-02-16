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

    def pull_lines(self, lines=None) -> list[dict]:
        if lines is None:
            lines = self.lines
        # return [{k: v} for n in lines for k, v in n.info.items()]
        line_list: list[dict] = []
        for line in lines:
            line_list.append(line.info)
        return line_list

    def write_centrex_lines(self, root_folder=''):
        if not root_folder:
            path = Path().cwd()
        else:
            path = Path(root_folder)
            if not path.is_dir():
                raise Exception(f'[Location.write_lines()]: {root_folder} is not a directory')

        # TODO: do the following sorting WITHIN info (make new Line labels)
        fiman_groups: dict[str, list[Line]] = dict()
        fiman_groups['UNASSIGNED'] = []
        fiman_groups['EMS'] = []
        s_ems = re.compile(r'(elev|elv|fire|facp)', re.IGNORECASE)

        fiman_empty = len(fiman_groups)
        for line in self.lines:
            if line['line_type'] == 'VOIP':
                continue

            fiman = line["Financial Manager"]
            if re.search(s_ems, line['Name']) or re.search(s_ems, line['Room']):
                fiman_groups['EMS'].append(line)
            elif not fiman:
                fiman_groups['UNASSIGNED'].append(line)
            elif fiman in fiman_groups.keys():
                fiman_groups[fiman].append(line)
            else:
                fiman_groups[fiman] = [line]

        # leave if there's no added lines
        if len(fiman_groups) == fiman_empty and len([ln for ln_list in fiman_groups.values() for ln in ln_list]) == 0:
            return None
        # remove empty groups
        fiman_groups = {k: ln_list for k, ln_list in fiman_groups.items() if ln_list}

        if re.search(r'(EM\s*PH|EP\s|EP\w{3,4}|EMER.*PHONE)', self.building):
            folder = path / 'EMERGENCY PHONES'
            if not folder.is_dir():
                folder.mkdir(parents=True, exist_ok=True)
            dicts_to_excel(folder / sanitize_filename(f'({len(self.lines)}) {self.building}'), self.pull_lines())
            return {"EMPH": self.pull_lines()}
        else:
            folder = path / sanitize_filepath(f"({len(self.lines)}) {self.building} [SLA {self.sla}]")
            folder.mkdir(parents=True, exist_ok=True)
            for fiman, lines in fiman_groups.items():
                centrex_sum: int = len([ln for ln in lines if ln['line_type'] != "VOIP"])
                filename = sanitize_filename(f'({centrex_sum}) {self.building} - {fiman}.xlsx')
                dicts_to_excel(folder / filename, self.pull_lines(lines))
            # write out a big sheet for all of them (if there's more than 1 sheet)
            if len(fiman_groups) > 1:
                dicts_to_excel(folder / sanitize_filename(f'({len(self.lines)}) {self.building} [ALL]'), self.pull_lines())

        return fiman_groups

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
