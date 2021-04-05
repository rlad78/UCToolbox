from fileops.excelOps.excelwriter import fix_imports
from .coordinates import Coordinate
import re


class Datablock:
    def __init__(self, data: list, force_header=False, fix_data=False) -> None:
        """Class for shaping and applying data within the wacky world of Excel.

        Args:
            data (list): Any 1D or 2D list, will be converted
                into nested lists of strings to represent
                Excel-like structure.
            force_header (bool=False): If data is a 2d list-list,
                setting this to True will treat the fist list as
                a header for the rest of the data. If data is a 
                list-dist, this value will be ignored.
            fix_data (bool=False): Applies a filter that will correct str
                values with ".0" at the end of them. This is done to correct
                the way Excel imports 'Number' values.
        """
        self.data: list[list[str]] = []  # data can remain empty!!
        self.header: list[str] = None
        try:
            datacopy = data.copy  # try not to mute origin data
        except AttributeError as e:
            raise Exception('[Datablock]: data is non-list type', e)
        
        if type(datacopy[0]) == list:
            if force_header:
                    self.header = datacopy.pop(0)
            for line in datacopy:
                temp_list: list[str] = []
                for item in line:
                    temp_list.append(item.__str__())
                self.data.append(temp_list)
            
        elif type(datacopy[0]) == dict:
            self.header = [x.__str__() for x in datacopy[0].keys()]
            for line in datacopy:
                temp_list: list[str] = []
                for value in line.values():
                    temp_list.append(value.__str__())
                self.data.append(temp_list)
        
        else:
            self.data.append([x.__str__() for x in datacopy])
            
        if fix_imports:
            for line in self.data:
                for value in line:
                    match_decimal = re.match(r'(\d+)\.0+', value)
                    if match_decimal:
                        value = match_decimal.group(1)
                    elif value == 'None':
                        value = ''
            
    def position(self, start_point) -> tuple[Coordinate, Coordinate]:
        """Given a starting-point, returns the coordinates for the range that
        would be taken up by the datablock.

        Args:
            start_point (tuple[int, int] or Coordinate): The starting point where
            the data will be inserted.

        Raises:
            TypeError: Raised if start_point is not one of the listed types.

        Returns:
            tuple[Coordinate, Coordinate]: Start-end pair of Coordinate values.
        """
        if type(start_point) == Coordinate:
            y1, x1 = start_point.pos()
        elif type(start_point) == tuple:
            y1, x1 = start_point
        else:
            raise TypeError(f"[Datablock]: unrecognized start_point type '{type(start_point)}'")
        
        y2 = y1 + len(self.data)
        x2 = x1 + max([len(n) for n in self.data])
        return Coordinate(y1, x1), Coordinate(y2, x2)
    
    def constrict(self, height=-1, width=-1):
        """Removes any data that does not fit into the height and width
        constraints given. This WILL remove data.

        Args:
            height (int): Defaults to data's height if left at -1.
            width (int): Defaults to data's width if left at -1.
        """
        if height < 0:
            height = len(self.data)
        if width < 0:
            width = max([len(n) for n in self.data])
        
        shaped_data: list[list[str]] = []
        if self.header is not None:
            self.header = self.header[:width]
        for line in self.data[:height]:
            shaped_data.append(line[:width])
            
        self.data = shaped_data
    
    def dictlist(self) -> list[dict]:
        """Returns a list of dictionaries with the values in the datablock.
        If the datablock has no header, assigns keys of 'Value n' where 'n'
        ranges from 1 to the width of the datablock.

        Returns:
            list[dict]: Datablock represented in lists of dictionaries.
        """
        dict_list: list[dict] = []
        keys: list[str] = []
        if self.header is not None:
            keys = self.header
        else:
            keys = [f'Value {n+1}' for n in range(max([len(n) for n in self.data]))]
        
        for line in self.data:
            temp_dict: dict = {}
            for i, value in enumerate(line):
                temp_dict[keys[i]] = value
            dict_list.append(temp_dict)
        
        return dict_list
    
    def listlist(self) -> list[list[str]]:
        """Returns data in datablock. If there is a header, inserts header
        at the top of the data.

        Returns:
            list[list[str]]: Datablock represented by nested list.
        """
        if self.header is not None:
            temp_list = self.header
            temp_list.append(self.data)
            return temp_list
        else:
            return self.data
    