from .sourcedata import SourceData


# CSV HEADER LABELS
DN = 'Telephone Number'
POSITION = 'Key'
BLF_NUMBER = 'BLFDN'


class BLF(SourceData):
    def __init__(self, blf_data: list[dict]):
        super(BLF, self).__init__(blf_data)
        if not self._data[0][DN].isnumeric():
            self._format_phone_numbers(DN, BLF_NUMBER)

    def get_blfs(self, phone_number: str) -> list[str]:
        all_blfs = self._findall(BLF_NUMBER, DN, phone_number)
        return [x for x in all_blfs if x != phone_number]
