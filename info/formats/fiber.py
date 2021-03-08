from datatypes import SourceData
import re


BUILDING = "Buildings"

class FIBER(SourceData):
    def __init__(self, source: list[dict]):
        super().__init__(source)
        
    def check_fiber_facp(self, building_name: str) -> bool:
        found = self._parse(BUILDING, building_name, re.I)
        if found:
            return True
        return False