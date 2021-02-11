from .sourcedata import SourceData


# CSV HEADER LABELS
BLF_DN = 'Telephone Number'
BLF_POSITION = 'Key'
BLF_NUMBER = 'BLFDN'


class BLF(SourceData):
    def __init__(self, blf_data: list[dict]):
        super(BLF, self).__init__(blf_data)
        if not self._data[0][BLF_DN].isnumeric():
            self._format_phone_numbers(BLF_DN, BLF_NUMBER)

    def get_blfs(self, phone_number: str) -> list[str]:
        all_blfs = self._findall(BLF_NUMBER, BLF_DN, phone_number)
        return [x for x in all_blfs if x != phone_number]


# CSV HEADER LABELS
BSET_HEADER = 'Column1'


class BSET(SourceData):
    def __init__(self, bset_data: list[dict]):
        super(BSET, self).__init__(bset_data)
        if not self._data[0][BSET_HEADER].isnumeric():
            self._format_phone_numbers(BSET_HEADER)

    def is_bset(self, phone_number) -> bool:
        if self._get(BSET_HEADER, phone_number):
            return True
        else:
            return False


# CSV HEADER LABELS
CFD_DN = 'Telephone Number'
CFD_BUSY_FORWARD = 'CFBTN'
CFD_NO_ANSWER_FORWARD = 'CFDTN'


class CFD(SourceData):
    def __init__(self, cfd_data: list[dict]):
        super(CFD, self).__init__(cfd_data)
        self._format_phone_numbers(CFD_DN, CFD_NO_ANSWER_FORWARD)

    def get_forwarding(self, phone_number: str) -> str:
        return self._find(CFD_NO_ANSWER_FORWARD, CFD_DN, phone_number)


# CSV HEADER LABELS
CPG_GROUP = 'Call Pickup Group Number'
CPG_GROUP_LEN = 'Number of Lines'
CPG_DN = 'Telephone Number'


class CPG(SourceData):
    def __init__(self, cpg_data: list[dict]):
        super(CPG, self).__init__(cpg_data)
        if not self._data[0][CPG_DN].isnumeric():
            self._format_phone_numbers(CPG_DN)
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
            if entry[CPG_GROUP]:
                if current_group and current_cpg_num != '0':
                    self.__cpg_groups[current_cpg_num] = current_group.copy()
                    current_group = []
                current_cpg_num = entry[CPG_GROUP]
            current_group.append(entry[CPG_DN])


# CSV HEADER LABELS
LA_DN = 'Telephone Number'
LA_KEY = 'Key'
LA_LINE = 'KTN'


class LA(SourceData):
    def __init__(self, la_data: list[dict]):
        super(LA, self).__init__(la_data)
        if not self._data[0][LA_DN].isnumeric():
            self._format_phone_numbers(LA_DN)

    def get_las(self, phone_number: str) -> list[str]:
        all_las: list[str] = self._findall(LA_LINE, LA_DN, phone_number)
        return [x for x in all_las if x != phone_number]
