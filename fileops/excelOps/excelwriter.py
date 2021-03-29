import xlwings as xlw
from pathlib import Path
import random
import re
from .xlinterface import XLInterface
# from .coordinates import Coordinate
# from datatypes import ResultData

FILETYPES: list[str] = ['.xlsx', '.xlsm', '.xls']


class ExcelWriter(XLInterface):
    def __init__(self, filename, directory="") -> None:
        super().__init__()
        self.__current_sheet: xlw.Sheet = None
        self.__table_style_index = 0
        if directory:
            p = Path(directory)
        else:
            p = Path().cwd()
        self.new(p / filename)

    def new(self, filepath: Path):
        self.book = xlw.Book()
        self.active = True
        self.__current_sheet = self.book.sheets.active
        if filepath.parent.is_dir() and filepath.parent.exists():
            if filepath.suffix not in FILETYPES:
                filepath = filepath.with_suffix('.xlsx')
            self.book.save(str(filepath))
        else:
            raise Exception(f'Could not save {filepath}: invalid directory')

    def new_sheet(self, name, position=-1) -> xlw.Sheet:
        if not name:
            name = f'{random.random():.10f}'.replace("0.", "")
        if position > 0 and position < len(self.book.sheets):
            self.book.sheets.add(name, before=self.book.sheets[position])
            self.__current_sheet = self.book.sheets.active
            
    def change_sheet(self, index=-1, name=''):
        self.__current_sheet = super()._get_sheet(index, name)

    def delete_sheet(self, index=0, name='') -> bool:
        sht = self.get_sheet(index, name)

        if sht is not None:
            sht.delete()
            return True
        else:
            print(f'[{__name__}.delete_sheet]: tried deleting sheet "{name if name else index}" but was not found')
            return False
    
    def write_range(self, data: list, start_point: tuple[int, int], end_point=None, sheet=None, headers=True) -> xlw.Range:
        # let's NOT work with negatives or zero
        points = start_point + end_point if end_point is not None else start_point
        if not all([bool(x > 0) for x in points]):
            print(f"[write_range] negative or zero coordinate was attempted: {start_point=} {end_point=}")
            return None
        
        # figure out which sheet we're writing to
        wanted_sheet: xlw.Sheet = sheet if sheet is not None else self.__current_sheet
        wanted_range = wanted_sheet.range(start_point, end_point)
        
        # format nested lists to insert into range
        data_array: list[list[str]] = []
        if type(data[0]) == dict:
            if headers:
                data_array.append([x.__str__() for x in data[0].keys()])
            for entry in data:
                data_array.append([x.__str__() for x in entry.values()])
        elif type(data[0]) == list:
            for row in data:
                data_array.append([x.__str__() for x in row])
        elif data is None:
            print(f'[{__name__}.write_range]: given empty data, wrote nothing!')
            return None
        else:  # 1d list
            data_array.append([x.__str__() for x in data])
            
        # shape data to fit within dimensions of end_point
        if end_point is not None:
            width = len(wanted_range.columns)
            height = len(wanted_range.rows)
            new_array: list[list[str]] = []
            for h, row in enumerate(data_array):
                if h == height:
                    break
                new_array.append(row[:width])
            data_array = new_array
        
        # apply data write, return written range
        wanted_range.value = data_array
        return wanted_sheet.range(*data_range(data_array, start_point))
        
    def write_table(self, data: list[dict], sheet=None) -> int:
        if sheet is None:
            sheet = self.__current_sheet
        
        # check for existing tables, we'll put new table below
        bottom_row_index = -1
        if len(sheet.tables) > 0:
            for table in sheet.tables:
                last_row: int = table.data_body_range.last_cell.row
                if last_row > bottom_row_index:
                    bottom_row_index = last_row
        
        table_range = self.write_range(data, (bottom_row_index+2, 1), sheet=sheet)
        sheet.tables.add(table_range, table_style_name=self._table_style())
        table_range.table.range.autofit()
        return len(sheet.tables)
    
    def append_table(self, data: list[dict], sheet=None, table_index=0):
        if sheet is None:
            sheet = self.__current_sheet
            
        table_range: xlw.Range = sheet.tables[table_index].range
        start_row: int = table_range.last_cell.offset(row_offset=1).row
        data_coords = data_range(data, (start_row, 1))
        end_row: int = data_coords[1][0]
        
        sheet.range(f'{start_row}:{end_row}').insert('down')
        self.write_range(data, (start_row, 1), sheet=sheet, headers=False)
        table_range.table.range.autofit
    
    def get_table_data(self, table_index=0, sheet=None) -> list[dict]:
        if sheet is None:
            sheet = self.__current_sheet
            
        wanted_table: xlw.main.Table = sheet.tables[table_index]
        return nested_to_dict(wanted_table.range.value)        
    
    def edit_table(self, entry_match: str, edit_category: str, new_value: str):
        pass
    
    def _check_range_empty(self, start_point: tuple[int, int], end_point: tuple[int, int]) -> bool:
        pass
    
    def _table_style(self) -> str:
        # uses 8 through 14
        index = (self.__table_style_index % 7) + 8
        self.__table_style_index += 1
        return f'TableStyleLight{index}'


def data_range(data: list, start_point: tuple[int, int]) -> tuple[tuple[int,int], tuple[int,int]]:
    max_width = max([len(a) for a in data])
    height = len(data)
    end_point: tuple[int, int] = start_point[0] + height -1, start_point[1] + max_width - 1
    return start_point, end_point

def data_format(data, height=0, width=0, headers=True) -> list[list[str]]:
    data_array: list[list[str]] = []
    if type(data[0]) == dict:
        if headers:
            data_array.append(data.keys())
        for entry in data:
            data_array.append([x.__str__() for x in entry.values()])
    elif type(data[0]) == list:
        for row in data:
            data_array.append([x.__str__() for x in row])
    elif data is None:
        return None
    else:  # 1d list
        data_array.append([x.__str__() for x in data])
        
    return data_array

def nested_to_dict(nest: list[list[str]]) -> list[dict]:
    keys = nest[0]
    out_list: list[dict] = []
    for entry in nest[1:]:
        new_dict = {}
        for i, value in enumerate(entry):
            new_dict[keys[i]] = fix_imports(value.__str__())
        out_list.append(new_dict)
    return out_list

def fix_imports(value: str) -> str:
    match_decimal = re.match(r'(\d+)\.0+', value)
    if match_decimal:
        return match_decimal.group(1)
    elif value == 'None':
        return ''
    else:
        return value
