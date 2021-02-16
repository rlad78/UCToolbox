import concurrent.futures as fut
from typing import Any


def new_pool() -> dict:
    pool_bundle: dict = {}
    pool_bundle['pool'] = fut.ThreadPoolExecutor
    pool_bundle['futures']: dict[str, fut.Future] = {}
    return pool_bundle


def pool_add(pool: dict, name: str, job, *args) -> None:
    exec: fut.ThreadPoolExecutor = pool['pool']
    fut_list: dict[str, fut.Future] = pool['futures']
    fut_list[name] = exec.submit(job, *args)


def pool_get(pool: dict) -> dict:
    fut_list: dict[str, fut.Future] = pool['futures']
    get_contents: dict = {}
    for name, contents in fut_list:
        get_contents[name] = contents.result()
    return get_contents


def open_files(files: list[tuple[str, str]], open_func) -> dict:
    """
    :param files: list of (label, file) tuples
    """
    futures: dict[str, fut.Future] = {}
    file_list: dict = {}
    getter = fut.ThreadPoolExecutor()
    for label, file in files:
        futures[label] = getter.submit(open_func, file)
    for key, contents in futures.items():
        file_list[key] = contents.result()
    return file_list


def save_files(data: dict[str, Any], save_func) -> None:
    """
    :param data: dict[filepath, dataset]
    """
    futures: dict[str, fut.Future] = {}
    saver = fut.ThreadPoolExecutor()
    for filepath, dataset in data:
        saver.submit(save_func, filepath, dataset)
