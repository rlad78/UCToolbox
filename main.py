from datatypes import Line, Location
from info import Dataset, Database
from actions import db, data


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
    buildings = database.lines_by_building()
    for sla, building in buildings.items():
        building.write_centrex_lines('/Users/arf/PycharmProjects/UCToolbox/OUTPUT')
        print(f'Printed {len(building.lines)} lines from {building.building}')
        input()


if __name__ == '__main__':
    # csv_from_dicts('ucdb.csv', generate_db(load_dataset()))
    # print(search_line_demo(input('Phone number: ')))
    # preview_buildings(data.load_dataset())
    write_buildings(data.load_dataset())