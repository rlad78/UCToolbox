from .line import Line
from IO import dicts_to_excel
from pathlib import Path
from pathvalidate import sanitize_filename


class Location:
    def __init__(self, building_data: dict = None):
        self._categories: list[str] = [
            "Name", "Building ID",
            "SLA", "Address"
        ]
        self._info = {k: '' for k in self._categories}
        self.lines: list[Line] = []
        if building_data is not None:
            self.update(building_data)

    def __str__(self):
        out: str = f'{self._info["Building"]} (SLA {self._info["SLA"]}, {self._info["Building ID"]})\n'
        out += self._info['Address']

    def __getitem__(self, item):
        return self._info[item]

    def update(self, info: dict) -> None:
        for key, value in info.items():
            if key not in self._categories:
                raise Exception(f'[Location]: "{key}" not a valid location category')
            self._info[key] = value

    def add_line(self, line: Line) -> None:
        if line is not None:
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
        filename = sanitize_filename(self._info['Building'] + '.xlsx')
        dicts_to_excel(path / filename, self.pull_lines())
