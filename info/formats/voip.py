from datatypes.sourcedata import SourceData, Entry
from typing import Union


# CSV HEADER LABELS
DEVICE_NAME = 'DEVICE NAME'
NAME = 'DESCRIPTION'
USERID = 'OWNER USER ID'
DN = 'DIRECTORY NUMBER 1'


class VOIPEntry(Entry):
    def __init__(self, voip_entry: dict):
        super(VOIPEntry, self).__init__(voip_entry)
        self.device_name = voip_entry[DEVICE_NAME]
        self.description = voip_entry[NAME]
        self.user_id = voip_entry[USERID]
        self.dn = voip_entry[DN]


class VOIP(SourceData):
    def __init__(self, voip_data: list[dict]):
        super(VOIP, self).__init__(voip_data)

    def get_phone(self, phone_number: str) -> Union[VOIPEntry, None]:
        this_voip = self._get(DN, phone_number)
        if this_voip:
            return VOIPEntry(this_voip)
        else:
            return None
