import csv
import concurrent.futures
# import re


def csv_to_list(file_name: str) -> list[list[str]]:
    with open(file_name, encoding="utf-8-sig") as csv_file:
        return list(csv.reader(csv_file, delimiter=","))


def csv_to_dicts(file_name: str) -> list[dict]:
    with open(file_name, encoding="utf-8-sig") as csv_file:
        return list(csv.DictReader(csv_file, delimiter=","))


def csv_from_dicts(file_name: str, dict_lines: list[dict]):
    with open(file_name, mode='w', newline='') as csv_file:
        fieldnames: list[str] = list(dict_lines[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(dict_lines)
        print(f'Wrote {len(dict_lines)} lines to {csv_file.name}')


def csv_from_list(file_name: str, head: list[str], lines: list[list[str]]):
    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(head)
        writer.writerows(lines)
        print(f'Wrote {len(lines)} lines to {csv_file.name}')


#
# def get_valid_filename(s: str) -> str:
#     s = str(s).strip().replace(' ', '_')
#     return re.sub(r'(?u)[^-\w.]', '', s)


def get_csv_stack(files: list[tuple[str, str]]) -> dict:
    """
    :param files: list of (label, filepath) tuples
    """
    futures = {}
    return_dicts = {}
    getter = concurrent.futures.ThreadPoolExecutor()
    for label, file in files:
        futures[label] = getter.submit(csv_to_dicts, file)
    for key, contents in futures.items():
        return_dicts[key] = contents.result()
    return return_dicts
