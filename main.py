from datatypes import Line, Location
from info import Dataset, Database
from actions import db, data
from fileops import csv_from_dicts
from pathlib import Path


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


def write_buildings(dataset=None):
    database: Database = db.get_db(dataset)
    buildings = database.centrex_by_building()
    output_folder = Path().cwd() / "OUTPUT"
    # make it empty
    if output_folder.is_dir():
        rm_dir(str(output_folder))

    results: dict[str, dict] = {
        "Emergency Phones": {"Building": "Emergency Phones", "Line Count": 0, "Elevator(s)?": ""}
    }
    output_folder.mkdir(parents=True, exist_ok=True)
    for sla, building in buildings.items():
        building.write_centrex_lines(str(output_folder))
        print(f'Printed {len(building.lines)} lines from {building.building}')

        info = building.summary()
        if info["EMPH"]:
            results['Emergency Phones']['Line Count'] += info['Line Count']
        else:
            results[building.building] = {k: v for k, v in info.items() if k != "EMPH"}
    summary_file = output_folder / "SUMMARY.csv"
    csv_from_dicts(str(summary_file), [d for d in results.values()])

if __name__ == '__main__':
    # csv_from_dicts('ucdb.csv', generate_db(load_dataset()))
    # print(search_line_demo(input('Phone number: ')))
    # preview_buildings(data.load_dataset())
    write_buildings(data.load_dataset())