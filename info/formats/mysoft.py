from .sourcedata import SourceData


# CSV HEADER LABELS
DN = 'UserID'
NAME = 'FirstName'
GL = 'GLNumber'
FLOOR = 'Floor'
ROOM = 'Room'
BLDG_ID = 'BuildingId'


class MYSOFT(SourceData):
    def __init__(self, mysoft_data: list[dict]):
        super(MYSOFT, self).__init__(mysoft_data)

    def get_line(self, phone_number: str) -> dict:
        return self.get(DN, phone_number)
