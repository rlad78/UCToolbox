from datatypes import Line
from info import Database
from . import db, data
from fileops import *
from pathvalidate import sanitize_filename
import re


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
        building_folder.mkdir(parents=True, exist_ok=True)
        for fiman, lines in fiman_lines.items():
            dicts_to_excel(building_folder / sanitize_filename(f'({len(lines)}) {building.building} - {fiman}.xlsx'), lines)

        # print out an ALL sheet
        dicts_to_excel(building_folder / sanitize_filename(f'({len(building.lines)}) {building.building} - ALL.xlsx'), building.pull_lines())
        print(f'Printed {len(building.lines)} lines from {building.building}')

        info = building.summary()
        if info["EMPH"]:
            results['Emergency Phones']['Line Count'] += info['Line Count']
        else:
            results[building.building] = {k: v for k, v in info.items() if k != "EMPH"}

    summary_file = output_folder / "SUMMARY.csv"
    csv_from_dicts(str(summary_file), [d for d in results.values()])
    

def write_fire(dataset=None):
    database: Database = db.get_db(dataset)
    fire_temp: list[dict] = database.parseall("Name", r'(fire|facp)', re.I)
    fire_temp += (database.parseall("Name", r'(fire|facp)', re.I))

    #remove duplicates and voip lines
    fire_lines: list[dict] = []
    fire_dns: list[str] = []
    for line in fire_temp:
        if line['Phone Number'] not in fire_dns and line['line_type'] != 'VOIP':
            fire_lines.append(line)
            fire_dns.append(line['Phone Number'])

    p = get_output_folder()
    dicts_to_excel(p / "FIRE ALARMS.xlsx", fire_lines, sheet_name="FIRE")
