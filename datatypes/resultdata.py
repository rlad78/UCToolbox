from fileops import *
from pathlib import Path
from pandas import DataFrame
from typing import Union
import re


UNIQUE_IDENT = "Phone Number"

class ResultData:
    def __init__(self, data: list[dict], name: str, exclude='') -> None:
        self.data: list[dict] = data  # DO NOT WRITE OVER THIS
        self.name: str = name
        self.exclude: list[str] = exclude.replace(', ', ',').split(',')
        self.__group_func: dict[str, function] = {
            "VoIP": self.__get_voip,
            "Centrex": self.__get_centrex,
            "Elevator": self.__get_elevator,
            "Fire": self.__get_fire
        }
        if self.data and self.exclude:
            for remove in self.exclude:
                if remove in self.__group_func:
                    self.__del_from_data(self.__group_func[remove]())
        
    def __iter__(self):
        for d in self.data:
            yield d
            
    def __getitem__(self, key):
        for d in self.data:
            if d[UNIQUE_IDENT] == key:
                return d
        else:
            raise KeyError(f'{key=} does not exist in ResultData({self.name})')
    
    def to_csv(self, filepath='', dirpath='') -> None:
        p = get_path(self.name, filepath, dirpath)
        
        if p is not None:
            csv_from_dicts(str(p), self.data)
            
    def to_excel(self, filepath='', dirpath='') -> None:
        p = get_path(self.name, filepath, dirpath)
        
        if p is not None:
            dicts_to_excel(str(p), self.data)
            
    def dataframe(self, columns=[]) -> DataFrame:
        try:
            requested_columns: list[str] = []
            for col in columns:
                if col in self.data[0].keys():
                    requested_columns.append(col)
            if len(requested_columns) == 0:
                requested_columns = [x for x in self.data[0].keys()]
        except KeyError:
            return DataFrame()  # if there's no data, return empty DF
        return DataFrame(self.data, columns=columns)
    
    def __get_by_match(self, regex: str, cateogry: str) -> list[dict]:
        wanted_data: list[dict] = []
        for entry in self.data:
            if re.search(regex, entry[cateogry], re.I):
                wanted_data.append(entry)
        return wanted_data

    def __get_by_multiple(self, re_cat: list[tuple[str, str]]) -> list[dict]:
        wanted_data: list[dict] = []
        for entry in self.data:
            matches = [re.search(regex, entry[cat], re.I) for regex, cat in re_cat]
            if any(matches):
                wanted_data.append(entry)
        return wanted_data
    
    def __del_from_data(self, items: list[dict]) -> None:
        del_candidates: list[str] = [x[UNIQUE_IDENT] for x in items]
        if not del_candidates:
            return None
        
        new_data: list[dict] = []
        for entry in self.data:
            if entry[UNIQUE_IDENT] not in del_candidates:
                new_data.append(entry)
        self.data = new_data
        
    
    def __get_voip(self) -> list[dict]:
        return self.__get_by_match(r'voip', 'line_type')
        
    def __get_centrex(self) -> list[dict]:
        return self.__get_by_match(r'centrex', 'line_type')
    
    def __get_fire(self) -> list[dict]:
        searches = [
            (r'(fire|facp)', 'Name'),
            (r'(fire|alarm|alrm)', 'Room')
        ]
        return self.__get_by_multiple(searches)
    
    def __get_elevator(self) -> list[dict]:
        searches = [
            (r'(elev|elv)', 'Name'),
            (r'(ele|elv)', 'Room')
        ]
        return self.__get_by_multiple(searches)
            

def get_path(name, filepath='', dirpath='') -> Union[None, Path]:
    if dirpath:
        p = Path(dirpath)
        if p.is_dir():
            p = p / f'{name}.csv'
        else:
            print(f'Could not save {name}.csv, {dirpath=} is invalid.')
            p = None
    elif filepath:
        p = Path(filepath)
        if p.parent.is_dir():
            if p.suffix != '.csv':
                p = p.with_suffix('.csv')
        else:
            print(f'Could not save {p.name}, path {filepath} is invalid.')
            p = None
    else:
        p = Path().cwd() / f'{name}.csv'
