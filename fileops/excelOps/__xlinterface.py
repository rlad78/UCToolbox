import xlwings as xlw
from pathlib import Path
from typing import Union

FILETYPES: list[str] = ['.xlsx', '.xlsm', '.xls']


class XLInterface:
    def __init__(self) -> None:
        self.active: bool = False
        self.book: xlw.Book = None
        
    def __bool__(self) -> bool:
        return self.active

    def open(self, filepath: Path, read_only=False, password=""):
        # excel_file: Path = Path(filepath)
        if filepath.is_file and filepath.suffix in FILETYPES:
            if password:
                self.book = xlw.Book(str(filepath), read_only=read_only, password=password)
            else:
                self.book = xlw.Book(str(filepath), read_only=read_only)
            self.active = True
        else:
            raise Exception(f'Failed to open {filepath}, file not found')
    
    def close(self) -> bool:
        if self.book is not None:
            self.book.close
            self.__init__()
            return True
        else:
            return False
            
    def _get_sheet(self, index=-1, name='') -> xlw.Sheet:
        sht: xlw.Sheet
        if index != -1:
            try:
                sht = self.book.sheets[index]
            except IndexError:
                raise Exception(f'[{__name__}.get_sheet]: tried getting sheet {index} when there ' +
                      f'is/are only {len(self.book.sheets)} sheet(s)')
        elif name:
            for sheet in self.book.sheets:
                if sheet.name == name:
                    sht = sheet
                    break
            else:
                raise Exception(f'[{__name__}.get_sheet]: tried getting sheet but "{name}" was not found')
        return sht
