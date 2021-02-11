from .sourcedata import SourceData


# CSV HEADER LABELS
HEADER = 'Column1'


class BSET(SourceData):
    def __init__(self, bset_data: list[dict]):
        super(BSET, self).__init__(bset_data)
        if not self._data[0][HEADER].isnumeric():
            self._format_phone_numbers(HEADER)

    def is_bset(self, phone_number) -> bool:
        if self._get(HEADER, phone_number):
            return True
        else:
            return False
