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
