from .sourcedata import SourceData


# CSV HEADER LABELS
DEVICE_NAME = 'DEVICE NAME'
NAME = 'DESCRIPTION'
USERID = 'OWNER USER ID'
DN = 'DIRECTORY NUMBER 1'


class VOIP(SourceData):
    def __init__(self, voip_data: list[dict]):
        super(VOIP, self).__init__(voip_data)

    def get_phone(self, phone_number: str) -> dict:
        return self.get(DN, phone_number)
