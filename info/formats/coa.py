from .sourcedata import SourceData, Entry
from typing import Union

# CSV HEADER LABELS
DEPT_NAME = "Department Name"
DEPT_ID = "Department ID"
FIMAN = "Financial Manager"


class COAEntry(Entry):
    def __init__(self, coa_entry: dict):
        super(COAEntry, self).__init__(coa_entry)
        self.financial_manager = coa_entry[FIMAN]
        self.department = coa_entry[DEPT_NAME]
        self.dept_id = coa_entry[DEPT_ID]


class COA(SourceData):
    def __init__(self, coa_data: list[dict]):
        super(COA, self).__init__(coa_data)

    def find_fiman(self, department_id: str) -> str:
        return self._find(FIMAN, DEPT_ID, department_id)

    def find_all_fiman_dept(self, financial_manager: str) -> list[str]:
        return self._findall(DEPT_ID, FIMAN, financial_manager)

    def get_dept(self, department_id: str) -> Union[COAEntry, None]:
        this_dept = self._get(DEPT_ID, department_id)
        if this_dept:
            return COAEntry(this_dept)
        else:
            return None
