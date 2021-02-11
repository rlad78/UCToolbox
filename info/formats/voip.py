from .sourcedata import SourceData


class VOIP(SourceData):
    # CSV HEADER LABELS
    DEVICE_NAME = 'DEVICE NAME'
    NAME = 'DESCRIPTION'
    USERID = 'OWNER USER ID'
    DN = 'DIRECTORY NUMBER 1'

    def __init__(self, voip_data: list[dict]):
        super(VOIP, self).__init__(voip_data)

    def get_phone(self, phone_number: str) -> dict:
        return self._get(self.DN, phone_number)
