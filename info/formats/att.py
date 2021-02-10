# GLOBALS
SLA_NBR = 'SLA'
ADDRESS = 'SLA Address'
LINE_TYPE = 'USOC'
DN = 'TN'
LOCATION = 'LOC'


class ATT:
    def __init__(self, att_data: list[dict]):
        self._data = att_data

    def __iter__(self):
        for entry in self._data:
            yield entry
