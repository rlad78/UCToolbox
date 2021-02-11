from .sourcedata import SourceData


# CSV HEADER LABELS
DN = 'Telephone Number'
KEY = 'Key'
APPEARANCE = 'KTN'


class LA(SourceData):
    def __init__(self, la_data: list[dict]):
        super(LA, self).__init__(la_data)
        if not self._data[0][DN].isnumeric():
            self._format_phone_numbers(DN)

    def get_las(self, phone_number: str) -> list[str]:
        all_las: list[str] = self._findall(APPEARANCE, DN, phone_number)
        return [x for x in all_las if x != phone_number]
