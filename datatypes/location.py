from .line import Line
from .sourcedata import Entry
from fileops import dicts_to_excel
from pathlib import Path
from pathvalidate import sanitize_filename, sanitize_filepath


class Location(Entry):
    def __init__(self, building_data: dict):
        super(Location, self).__init__(building_data)
        self.building = building_data.get('Name', "")
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
            # return [{k: v} for n in self.lines for k, v in n.info.items()]
            return []
        elif type(lines) == list and lines and type(lines[0]) == Line:
            # return [{k: v} for n in lines for k, v in n.info.items()]
            line_list: list[dict] = []
            for line in lines:
                line_list.append(line.info)
            return line_list
        else:
            return []

    def write_centrex_lines(self, root_folder=''):
        if not root_folder:
            path = Path().cwd()
        else:
            path = Path(root_folder)
            if not path.is_dir():
                raise Exception(f'[Location.write_lines()]: {root_folder} is not a directory')

        fiman_groups: dict[str, list[Line]] = dict()
        fiman_groups['UNASSIGNED'] = []
        for line in self.lines:
            if line['line_type'] == 'VOIP':
                continue
            fiman = line["Financial Manager"]
            if not fiman:
                fiman_groups['UNASSIGNED'].append(line)
            elif fiman in fiman_groups.keys():
                fiman_groups[fiman].append(line)
            else:
                fiman_groups[fiman] = [line]
        if len(fiman_groups) == 1:  # leave if there's no centrex lines
            return None

        folder = path / sanitize_filepath(f"({len(self.lines)}) {self.building} [SLA {self.sla}]")
        folder.mkdir(parents=True, exist_ok=True)
        for fiman, lines in fiman_groups.items():
            centrex_sum: int = len([ln for ln in lines if ln['line_type'] != "VOIP"])
            filename = sanitize_filename(f'({centrex_sum}) {self.building} - {fiman}.xlsx')
            dicts_to_excel(folder / filename, self.pull_lines(lines))
