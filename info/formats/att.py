from .sourcedata import SourceData


class ATT(SourceData):
    # CSV HEADER LABELS
    SLA_NBR = 'SLA'
    ADDRESS = 'SLA Address'
    LINE_TYPE = 'USOC'
    DN = 'TN'
    LOCATION = 'LOC'

    def __init__(self, att_data: list[dict]):
        super(ATT, self).__init__(att_data)
        if not self._data[0][self.DN].isnumeric():
            self.__format_phone_lines()

    def __format_phone_lines(self):
        for entry in self._data:
            if not entry[self.DN].isnumeric():
                entry[self.DN] = format_phone_number(entry[self.DN])

    def get_all_in_sla(self, sla: str) -> list[dict]:
        return self._getall(self.SLA_NBR, sla)

    def get_all_in_bldg(self, building_code: str) -> list[dict]:
        return self._parseall(self.LOCATION, rf'^bldg {building_code}')

    def get_line(self, phone_number: str) -> dict:
        return self._get(self.DN, phone_number)


def format_phone_number(number: str) -> str:
    ten_digit_number = ''
    for c in number:
        if c.isnumeric():
            ten_digit_number += c
    if len(ten_digit_number) != 10:
        return ''
    else:
        return ten_digit_number
