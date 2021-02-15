from .line import Line
from info.formats import SLAEntry
from IO import dicts_to_excel
from pathlib import Path
from pathvalidate import sanitize_filename, sanitize_filepath


class Location(SLAEntry):
    def __init__(self, building_data: dict):
        super(Location, self).__init__(building_data)
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
            return [{k: v} for n in self.lines for k, v in n.info]
        elif type(lines) == list and lines and type(lines[0]) == Line:
            return [{k: v} for n in lines for k, v in n.info]
        else:
            return []

    def write_lines(self, root_folder=''):
        if not root_folder:
            path = Path().cwd()
        else:
            path = Path(root_folder)
            if not path.is_dir():
                raise Exception(f'[Location.write_lines()]: {root_folder} is not a directory')

        fiman_groups: dict[str, list[Line]] = {}
        for line in self.lines:
            if line["Financial Manager"] in fiman_groups.keys():
                fiman_groups[line["Financial Manager"]].append(line)
            else:
                fiman_groups[list["Financial Manager"]] = list(line)
        for fiman, lines in fiman_groups.items():
            centrex_sum: int = len([ln for ln in lines if ln['line_type'] != "VOIP"])
            filename = sanitize_filename(f'({centrex_sum}) {self.building} - {fiman}.xlsx')
            dicts_to_excel(path / sanitize_filepath(self.building) / filename, self.pull_lines(lines))
