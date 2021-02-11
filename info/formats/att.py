from .sourcedata import SourceData, Entry
from typing import Union
import re

# CSV HEADER LABELS
SLA_NBR = 'SLA'
ADDRESS = 'SLA Address'
LINE_CODE = 'USOC'
DN = 'TN'
LOCATION = 'LOC'


class ATTEntry(Entry):
    def __init__(self, att_entry: dict):
        super(ATTEntry, self).__init__(att_entry)
        self.dn = att_entry[DN]
        self.sla = att_entry[SLA_NBR]
        self.address = att_entry[ADDRESS]
        self.bldg_code, self.room = split_loc(att_entry[LOCATION])
        self.floor = determine_floor(self.room)
        self.line_type = determine_line_type(att_entry[LINE_CODE])


class ATT(SourceData):
    def __init__(self, att_data: list[dict]):
        super(ATT, self).__init__(att_data)
        if not self._data[0][DN].isnumeric():
            self.__format_phone_lines()

    def __format_phone_lines(self):
        for entry in self._data:
            if not entry[DN].isnumeric():
                entry[DN] = format_phone_number(entry[DN])

    def get_all_in_sla(self, sla: str) -> list[ATTEntry]:
        all_lines: list[dict] = self._getall(SLA_NBR, sla)
        return [ATTEntry(x) for x in all_lines]

    def get_all_in_bldg(self, building_code: str) -> list[ATTEntry]:
        all_lines = self._parseall(LOCATION, rf'^bldg {building_code}')
        return [ATTEntry(x) for x in all_lines]

    def get_line(self, phone_number: str) -> Union[ATTEntry, None]:
        get_line = self._get(DN, phone_number)
        if get_line:
            return ATTEntry(get_line)
        else:
            return None


def split_loc(loc: str) -> (str, str):
    rm = ''
    bldg = ''

    bldg_match = re.search(r'BLDG (\S*);', loc)
    rm_match = re.search(r'RM (.*)$', loc)
    if bldg_match is not None:
        bldg = bldg_match.group(1)
    if rm_match is not None:
        rm = rm_match.group(1)
    return bldg, rm


def determine_floor(room: str) -> str:
    rm_numeric = ''.join([c for c in room if c.isnumeric()])
    if len(rm_numeric) >= 3 and room[0].isnumeric():
        return room[0]
    else:
        return ''


def determine_line_type(line_code: str) -> str:
    if re.search(r'^PR\w+', line_code):
        return 'VOIP'
    elif re.search(r'^M[14]\w+', line_code):
        return 'CENTREX'
    elif re.search(r'^CENAN', line_code):
        return 'DISCONNECTED'
    elif re.search(r'^ATNCS', line_code):
        return 'RESERVED'
    elif re.search(r'^M2\w+', line_code):
        return 'CONFERENCE BRIDGE'
    elif re.search(r'^LTQ8X', line_code):
        return 'ISDN'
    elif re.search(r'^ZZ7UK', line_code):
        return 'DATA'
    else:
        return f'UNKNOWN ({line_code})'


def format_phone_number(number: str) -> str:
    ten_digit_number = ''
    for c in number:
        if c.isnumeric():
            ten_digit_number += c
    if len(ten_digit_number) != 10:
        return ''
    else:
        return ten_digit_number
