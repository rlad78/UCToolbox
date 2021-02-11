from .sourcedata import SourceData


class HR(SourceData):
    # CSV HEADER LABELS
    DEPT = 'DEPTID'
    NAME = 'NAME'
    USERID = 'USERNAME'
    DN = 'WORK_PHONE'
    DUPLICATE = 'IS DUPLICATE?'

    def __init__(self, hr_data: list[dict]):
        super(HR, self).__init__(hr_data)
        if not self._data[0][self.USERID].islower():
            self.__userid_lowercase()

    def __userid_lowercase(self):
        for entry in self._data:
            entry[self.USERID] = entry[self.USERID].lower()

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
        results: list[dict] = self._getall(self.DN, phone_number)
        if len(results) == 1 and results[0][self.DUPLICATE] != 'YES':
            if dept_num and results[0][self.DEPT] != dept_num:
                return ''
            else:
                return results[0][self.USERID]
        else:
            return ''
