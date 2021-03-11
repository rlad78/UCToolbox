import xlwings as xlw
from pathlib import Path
import random
from .__xlinterface import XLInterface
from datatypes import ResultData

FILETYPES: list[str] = ['.xlsx', '.xlsm', '.xls']


class ExcelWriter(XLInterface):
    def __init__(self, filename, directory="") -> None:
        super().__init__()
        self.__current_sheet: xlw.Sheet = None
        if directory:
            p = Path(directory)
        else:
            p = Path().cwd()
        self.new(p / filename)

    def new(self, filepath: Path):
        self.book = xlw.Book()
        self.active = True
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
    
    def write_range(data: list[list], start_point: tuple[int, int], end_point=None, sheet=None):
        pass
        
    def write_table(data: ResultData, sheet=None) -> int:
        pass
    
    def append_table(data: ResultData, sheet=None, table_index=0):
        pass
    
    def edit_table(entry_match: str, edit_category: str, new_value: str):
        pass
    
    def _check_range_empty(start_point: tuple[int, int], end_point: tuple[int, int]) -> bool:
        pass
