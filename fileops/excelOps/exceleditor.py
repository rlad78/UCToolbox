from pathlib import Path
import xlwings as xlw
from .excelwriter import ExcelWriter
from .excelreader import ExcelReader


class ExcelEditor(ExcelReader, ExcelWriter):
    def __init__(self, filepath: Path, password="") -> None:
        super()._init_no_open()

            
