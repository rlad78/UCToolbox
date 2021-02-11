from .sourcedata import SourceData


class MYSOFT(SourceData):
    # CSV HEADER LABELS
    DN = 'UserID'
    NAME = 'FirstName'
    GL = 'GLNumber'
    FLOOR = 'Floor'
    ROOM = 'Room'
    BLDG_ID = 'BuildingId'

    def __init__(self, mysoft_data: list[dict]):
        super(MYSOFT, self).__init__(mysoft_data)

    def get_line(self, phone_number: str) -> dict:
        return self._get(self.DN, phone_number)
