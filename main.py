from datatypes import Line, Location
from info import Dataset, Database
from actions import db, data
from fileops import csv_from_dicts, dicts_to_excel
from pathlib import Path
from pathvalidate import sanitize_filename, sanitize_filepath
import re


def rm_dir(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_dir(child)
    pth.rmdir()


def search_line_demo(phone_number: str) -> Line:
    dataset = data.load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_line_all(phone_number))
    return me


# def preview_buildings(dataset: Dataset) -> None:
#     all_buildings: list[dict] = dataset.get_all_locations()
#     for loc in all_buildings:
#         print('')  # newline
#         print(Location(loc))
#         input('Press [enter]...')


def get_output_folder() -> Path:
    output_folder = Path().cwd() / "OUTPUT"
    # make it empty
    if output_folder.is_dir():
        rm_dir(str(output_folder))
        output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder


def write_buildings(dataset=None):
    database: Database = db.get_db(dataset)
    buildings = database.centrex_by_building()
    output_folder = get_output_folder()

    results: dict[str, dict] = {
        "Emergency Phones": {"Building": "Emergency Phones", "Line Count": 0, "Elevator(s)?": ""}
    }

    for sla, building in buildings.items():
        fiman_lines: dict[str, list[dict]] = building.pull_lines_by_fiman()
        total_lines: int = sum([len(n) for n in fiman_lines.values()])
        building_folder = output_folder / sanitize_filename(f'({total_lines}) {building.building} [SLA {sla}]')
        for fiman, lines in fiman_lines.items():
            dicts_to_excel(building_folder / sanitize_filename(f'({len(lines)}) {building.building} - {fiman}.xlsx'))

        # print out an ALL sheet
        dicts_to_excel(building_folder / sanitize_filename(f'({len(building.lines)}) {building.building} - ALL.xlsx'))
        print(f'Printed {len(building.lines)} lines from {building.building}')

        info = building.summary()
        if info["EMPH"]:
            results['Emergency Phones']['Line Count'] += info['Line Count']
        else:
            results[building.building] = {k: v for k, v in info.items() if k != "EMPH"}
    summary_file = output_folder / "SUMMARY.csv"
    csv_from_dicts(str(summary_file), [d for d in results.values()])

if __name__ == '__main__':
    write_fire(data.load_dataset())
