from .line import Line
from info.formats import SLAEntry
from IO import dicts_to_excel
from pathlib import Path
from pathvalidate import sanitize_filename


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

    def pull_lines(self) -> list[dict]:
        return [{k: v} for n in self.lines for k, v in n.info]

    def write_lines(self, root_folder=''):
        if not root_folder:
            path = Path().cwd()
        else:
            path = Path(root_folder)
            if not path.is_dir():
                raise Exception(f'[Location.write_lines()]: {root_folder} is not a directory')
        filename = sanitize_filename(self.data['Building'] + '.xlsx')
        dicts_to_excel(path / filename, self.pull_lines())
        # TODO: SORT THESE BY FIMAN!!!!!
