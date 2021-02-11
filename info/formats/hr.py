from .sourcedata import SourceData, Entry
from typing import Union
import Levenshtein

# CSV HEADER LABELS
DEPT = 'DEPTID'
NAME = 'NAME'
USERID = 'USERNAME'
DN = 'WORK_PHONE'
DUPLICATE = 'IS DUPLICATE?'


class HREntry(Entry):
    def __init__(self, hr_entry: dict):
        super(HREntry, self).__init__(hr_entry)
        self.dept_id = hr_entry[DEPT]
        self.name = hr_entry[NAME]
        self.user_id = hr_entry[USERID]
        self.dn = hr_entry[DN]
        self.is_duplicate = True if hr_entry[DUPLICATE] == 'YES' else False
        self.shortname = clean_proper(self.name)
        self.fullname = clean_full(self.name)


# TODO: Implement fuzzy name matching method in HR
class HR(SourceData):
    def __init__(self, hr_data: list[dict]):
        super(HR, self).__init__(hr_data)
        if not self._data[0][USERID].islower():
            self.__userid_lowercase()

    def __userid_lowercase(self):
        for entry in self._data:
            entry[USERID] = entry[USERID].lower()

    def find_user(self, phone_number: str, dept_num="", guess_name='') -> Union[HREntry, None]:
        # first, try to find a match with a dn
        dn_match = self._get(DN, phone_number)
        if dn_match:
            return HREntry(dn_match)

        # if no match, try to use dept_num to find all dept employees and do a fuzzy match
        if not dept_num or not guess_name:
            return None
        dept_matches: list[dict] = self._getall(DEPT, dept_num)
        dept_names: list[str] = [d[NAME] for d in dept_matches]
        winning_name = fuzzy_winner(guess_name, dept_names)
        if winning_name in dept_names:
            for user in dept_matches:
                if user[NAME] == winning_name:
                    return HREntry(user)
            else:
                raise Exception(f'[HR.find] winning user "{winning_name}" not in matches:\n{dept_matches}')
        else:
            return None

    def get_user(self, phone_number='', user_id='') -> Union[HREntry, None]:
        if user_id:
            this_user = self._get(USERID, user_id)
            if not this_user and phone_number:
                this_user = self._get(DN, phone_number)
        elif phone_number:
            this_user = self._get(DN, phone_number)
        else:
            raise Exception('[HR.get_user] tried to get user with no criteria')

        if this_user:
            return HREntry(this_user)
        else:
            return None


def fuzzy_winner(name: str, list_of_names: list[str]) -> str:
    winner: dict = {"score": 0.66, "name": name}
    for compare in list_of_names:
        comparison_score: float = fuzzy_value(name, compare)
        if comparison_score > winner["score"]:
            winner.update({"score": comparison_score, "name": compare})
    return winner["name"]


def fuzzy_value(name_1: str, name_2: str) -> float:
    searching_name: str = remove_punctuation(__proper_name_order(name_1))
    comparing_name: str = remove_punctuation(__proper_name_order(name_2))

    if not __all_alpha(name_1, name_2):
        return 0.0

    ratio_score: float = __ratio_str_value(searching_name, comparing_name)
    first_last_score: float = 0.0

    if ratio_score >= 0.45:
        first_last_score = __ratio_str_value(searching_name, __first_last_name(comparing_name))

    return ratio_score if ratio_score > first_last_score else first_last_score


# Carter Jr, Richard Lee -> Richard Lee Carter Jr
def clean_full(name: str) -> str:
    return remove_punctuation(__proper_name_order(name))


# Carter Jr, Richard Lee -> Richard Carter
def clean_proper(name: str) -> str:
    return remove_punctuation(__first_last_name(name))


def remove_punctuation(string_1: str, char_list: str = "._()") -> str:
    temp_str: str = string_1
    for c in char_list:
        temp_str.replace(c, "")
    return temp_str


def __proper_name_order(name: str) -> str:
    spaced_name: str = name
    spaced_name.replace(", ", ",")
    if ',' in name:
        name_parts: list[str] = spaced_name.split(",")
        if len(name_parts) > 2:
            return name
        else:
            return name_parts[1].strip() + " " + name_parts[0].strip()
    else:
        return name


def __ratio_str_value(name_1: str, name_2: str) -> float:
    corrected_name_1: str = __proper_name_order(name_1)
    corrected_name_2: str = __proper_name_order(name_2)

    bad_chars: str = "._()"
    for c in bad_chars:
        corrected_name_1.replace(c, "")
        corrected_name_2.replace(c, "")

    for word in corrected_name_1.split(" ") + corrected_name_2.split(" "):
        if not word.isalpha():
            return 0.0

    return Levenshtein.ratio(corrected_name_1.lower(), corrected_name_2.lower())


def __all_alpha(string_1: str, string_2: str) -> bool:
    examine_1: list[str] = remove_punctuation(__proper_name_order(string_1)).split(" ")
    examine_2: list[str] = remove_punctuation(__proper_name_order(string_2)).split(" ")

    for word in examine_1 + examine_2:
        if not word.isalpha():
            return False

    return True


def __first_last_name(name: str) -> str:
    ordered_name = name
    if ',' in name:
        ordered_name = __proper_name_order(name)

    if ordered_name.strip().count(' ') > 1:
        name_parts: list[str] = ordered_name.strip().split(" ")
        return name_parts[0] + " " + name_parts[-1]
    else:
        return ordered_name
