from .sourcedata import SourceData


class COA(SourceData):
    # CSV HEADER LABELS
    DEPT_NAME = "Department Name"
    DEPT_ID = "Department ID"
    FIMAN = "Financial Manager"

    def __init__(self, coa_data: list[dict]):
        super(COA, self).__init__(coa_data)

    def find_fiman(self, department_id: str):
        return self._find(self.FIMAN, self.DEPT_ID, department_id)

    def find_all_fiman_dept(self, financial_manager: str):
        return self._findall(self.DEPT_ID, self.FIMAN, financial_manager)
