from .sourcedata import SourceData


# CSV HEADER LABELS
SLA_NBR = 'SLA'
ADDRESS = 'SLA Address'
LINE_TYPE = 'USOC'
DN = 'TN'
LOCATION = 'LOC'


class ATT(SourceData):
    def __init__(self, att_data: list[dict]):
        super(ATT, self).__init__(att_data)
        if not self._data[0][DN].isnumeric():
            self.__format_phone_lines()

    def __format_phone_lines(self):
        for entry in self._data:
            if not entry[DN].isnumeric():
                entry[DN] = format_phone_number(entry[DN])

    def get_all_in_sla(self, sla: str) -> list[dict]:
        return self._getall(SLA_NBR, sla)

    def get_all_in_bldg(self, building_code: str) -> list[dict]:
        return self._parseall(LOCATION, rf'^bldg {building_code}')

    def get_line(self, phone_number: str) -> dict:
        return self._get(DN, phone_number)


def format_phone_number(number: str) -> str:
    ten_digit_number = ''
    for c in number:
        if c.isnumeric():
            ten_digit_number += c
    if len(ten_digit_number) != 10:
        return ''
    else:
        return ten_digit_number
