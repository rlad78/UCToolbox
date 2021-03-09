from . import SourceData
from fileops import *
from pathlib import Path
from pandas import DataFrame
from typing import Union
import re


UNIQUE_IDENT = "Phone Number"

class ResultData(SourceData):
    def __init__(self, data: list[dict], name: str, exclude='') -> None:
        super().__init__(data)
        self.name: str = name
        self.exclusions: list[str] = exclude.replace(', ', ',').split(',')
        self.__group_func: dict[str, function] = {
            "VoIP": self.__get_voip,
            "Centrex": self.__get_centrex,
            "Elevator": self.__get_elevator,
            "Fire": self.__get_fire
        }
        if self._data and self.exclusions:
            for remove in self.exclusions:
                if remove in self.__group_func:
                    self.__del_from_data(self.__group_func[remove]())
        
    # def __iter__(self):
    #     for d in self._data:
    #         yield d
            
    def __getitem__(self, key):
        for d in self._data:
            if d[UNIQUE_IDENT] == key:
                return d
        else:
            raise KeyError(f'{key=} does not exist in ResultData({self.name})')
        
    def __len__(self):
        return len(self._data)
    
    def __str__(self) -> str:
        s = self.name + '\n\n'
        s += self.dataframe().to_string()
        return s
    
    def to_csv(self, name: str, dirpath='') -> None:
        if not name:
            name = self.name
        p = get_path(name, '.csv', dirpath)
        
        if p is not None:
            csv_from_dicts(str(p), self._data)
            
    def to_excel(self, name: str, dirpath='', show_all_values=True) -> None:
        if not name:
            name = self.name
        p = get_path(name, '.xlsx', dirpath)
        
        if p is not None:
            dicts_to_excel(str(p), self._data, show_extra_cols=show_all_values)
            
    def dataframe(self, columns=[]) -> DataFrame:
        try:
            requested_columns: list[str] = []
            for col in columns:
                if col in self._data[0].keys():
                    requested_columns.append(col)
            if len(requested_columns) == 0:
                requested_columns = [x for x in self._data[0].keys()]
        except KeyError:
            return DataFrame()  # if there's no data, return empty DF
        return DataFrame(self._data, columns=requested_columns)
    
    def __get_by_match(self, regex: str, cateogry: str) -> list[dict]:
        wanted_data: list[dict] = []
        for entry in self._data:
            if re.search(regex, entry[cateogry], re.I):
                wanted_data.append(entry)
        return wanted_data

    def __get_by_multiple(self, re_cat: list[tuple[str, str]]) -> list[dict]:
        wanted_data: list[dict] = []
        for entry in self._data:
            matches = [re.search(regex, entry[cat], re.I) for regex, cat in re_cat]
            if any(matches):
                wanted_data.append(entry)
        return wanted_data
    
    def __del_from_data(self, items: list[dict]) -> None:
        del_candidates: list[str] = [x[UNIQUE_IDENT] for x in items]
        if not del_candidates:
            return None
        
        new_data: list[dict] = []
        for entry in self._data:
            if entry[UNIQUE_IDENT] not in del_candidates:
                new_data.append(entry)
        self._data = new_data
        
    
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
    
    def get_group(self, group: str):
        if group in self.__group_func:
            return ResultData(self.__group_func[group](), f'{self.name} - {group}')
        
    def remove_group(self, group: str) -> None:
        if group in self.__group_func:
            self.__del_from_data(self.__group_func[group]())
        
    def query(self, category_match_pairs: list[tuple[str,str]]):
        required_matches: dict = {k:v for k, v in category_match_pairs}
        return ResultData(super()._query(required_matches), f'{self.name} - Query')
    
    def parse(self, category: str, regex: str, flags=0):
        return ResultData(super()._parseall(category, regex, flags), f'{self.name} - Parse')

    def exclude(self, category: str, regex: str, flags=0):
        return ResultData(super()._exclude(category, regex, flags), f'{self.name} - Exclude')

    def group_by(self, group_type: str) -> dict:
        if group_type not in self._categories:
            return {}
        
        groups: dict[str, list[dict]] = {}
        for entry in self._data:
            if entry[group_type] in groups:
                groups[entry[group_type]].append(entry)
            else:
                groups[entry[group_type]] = [entry]
        return {k:ResultData(ent, f'{group_type}: {k}') for k, ent in groups.items()}

def get_path(name: str, extension: str, dirpath='') -> Union[None, Path]:
    if extension[0] != '.':
        extension = '.' + extension
        
    if dirpath:
        p = Path(dirpath)
        if p.is_dir():
            p = p / f'{name}{extension}'
        else:
            print(f'Could not save {name}{extension}, {dirpath=} is invalid.')
            p = None
    else:
        p = Path().cwd() / f'{name}{extension}'

    return p
