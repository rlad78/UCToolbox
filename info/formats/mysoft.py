from datatypes.sourcedata import SourceData, Entry
from typing import Union

# CSV HEADER LABELS
DN = 'UserID'
NAME = 'FirstName'
GL = 'GLNumber'
FLOOR = 'Floor'
ROOM = 'Room'
BLDG_ID = 'BuildingId'


class MYSOFTEntry(Entry):
    def __init__(self, mysoft_entry: dict):
        super(MYSOFTEntry, self).__init__(mysoft_entry)
        self.dn = mysoft_entry[DN]
        self.name = mysoft_entry[NAME]
        self.gl = mysoft_entry[GL]
        self.floor = mysoft_entry[FLOOR]
        self.room = mysoft_entry[ROOM]
        self.bldg_id = mysoft_entry[BLDG_ID]
        self.dept = dept_from_gl(self.gl)


class MYSOFT(SourceData):
    def __init__(self, mysoft_data: list[dict]):
        super(MYSOFT, self).__init__(mysoft_data)

    def get_line(self, phone_number: str) -> Union[MYSOFTEntry, None]:
        this_line = self._get(DN, phone_number)
        if this_line:
            return MYSOFTEntry(replace_null(this_line))
        else:
            return None


def dept_from_gl(gl: str) -> str:
    gl_parts: list[str] = gl.split('-')
    for part in gl_parts:
        if len(part) == 4 and part != '7009':
            return part
    else:
        return ''

def replace_null(entry: dict) -> dict:
    new_dict: dict = {}
    for k, v in entry.items():
        new_dict[k] = v if v != "NULL" else ""
    return new_dict
