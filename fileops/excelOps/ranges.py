import xlwings as xlw
from .coordinates import Coordinate
from .datablock import Datablock


def write_range(sheet: xlw.Sheet, data, start_point: tuple, end_point=None, headers=False) -> Coordinate:
    block = Datablock(data, force_header=headers)
    point1 = Coordinate(*start_point)
    
    if end_point is not None:
        point2 = Coordinate(*end_point)
        height, width = point1 - point2
        block.constrict(height, width)
    else:
        point2 = Coordinate(*block.position(start_point))
    
    sheet.range(start_point).value = block.listlist()
    return point2


def get_range_values(sheet: xlw.Sheet, start_point, end_point) -> list[list[str]]:
    block = Datablock(sheet.range(start_point, end_point).value, fix_data=True)
    return block.listlist()


def check_range_empty(sheet: xlw.Sheet, start_point, end_point) -> bool:
    for line in sheet.range(start_point, end_point).value:
        for value in line:
            if value is not None:
                return False
    return True
