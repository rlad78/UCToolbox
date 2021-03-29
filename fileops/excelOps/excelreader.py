from pathlib import Path
import xlwings as xlw
import pandas as pd
from .xlinterface import XLInterface


class ExcelReader(XLInterface):
    def __init__(self, filepath: Path, password="") -> None:
        super().__init__()
        super().open(filepath, read_only=True, password=password)
        
    def _init_no_open(self):
        super().__init__()

    def get_value(point: tuple[int, int]) -> str:
        pass
    
    def get_table(sheet=None, table_index=1) -> list[dict]:
        pass
    
    def find(value: str, sheet=None) -> tuple[int, int]:
        pass
    
    def search_workbook(value: str) -> tuple[str, int, int]:
        pass