from .sourcedata import SourceData


# CSV HEADER LABELS
GROUP = 'Call Pickup Group Number'
GROUP_LEN = 'Number of Lines'
DN = 'Telephone Number'


class CPG(SourceData):
    def __init__(self, cpg_data: list[dict]):
        super(CPG, self).__init__(cpg_data)
        if not self._data[0][DN].isnumeric():
            self._format_phone_numbers(DN)
        self.__get_groups()

    def get_cpg_lines(self, phone_number: str) -> list[str]:
        for group in self.__cpg_groups.values():
            if phone_number in group:
                return group
        else:
            return []

    def get_cpg_num(self, phone_number: str) -> str:
        for number, group in self.__cpg_groups.items():
            if phone_number in group:
                return number
        else:
            return ''

    def __get_groups(self):
        self.__cpg_groups: dict[str, list[str]] = {}
        current_cpg_num: str = '0'
        current_group: list[str] = []
        for entry in self._data:
            if entry[GROUP]:
                if current_group and current_cpg_num != '0':
                    self.__cpg_groups[current_cpg_num] = current_group.copy()
                    current_group = []
                current_cpg_num = entry[GROUP]
            current_group.append(entry[DN])
