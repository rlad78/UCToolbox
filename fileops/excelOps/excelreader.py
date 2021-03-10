from pathlib import Path
import xlwings as xlw
import pandas as pd
from .__xlinterface import XLInterface


class ExcelReader(XLInterface):
    def __init__(self, filepath: Path, password="") -> None:
        super().__init__()
        super().open(filepath, read_only=True, password=password)
        
    def _init_no_open(self):
        super().__init__()
