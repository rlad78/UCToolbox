from .sourcedata import SourceData, Entry
from typing import Union

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
        # TODO: get multiple versions of names using name str tools from VBAReplacer
        # self.shortname
        # self.fullname


class HR(SourceData):
    def __init__(self, hr_data: list[dict]):
        super(HR, self).__init__(hr_data)
        if not self._data[0][USERID].islower():
            self.__userid_lowercase()

    def __userid_lowercase(self):
        for entry in self._data:
            entry[USERID] = entry[USERID].lower()

    def find_user(self, phone_number: str, dept_num="") -> str:
        """
        Searches for an employee with a matching phone number and returns the
        user id of the employee. If search comes back with multiple results,
        returns empty str '' since duplicate number assignments have shown to be
        'main line' phone numbers and not tied to the user.

        :param phone_number: Any str of length 10
        :param dept_num: If not blank, used to make sure found user is in given dept
        :return: user id of matching employee if found, empty str otherwise
        """
        results: list[dict] = self._getall(DN, phone_number)
        if len(results) == 1 and results[0][DUPLICATE] != 'YES':
            if dept_num and results[0][DEPT] != dept_num:
                return ''
            else:
                return results[0][USERID]
        else:
            return ''

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
