from .sourcedata import SourceData


# CSV HEADER LABELS
DEPT_NAME = "Department Name"
DEPT_ID = "Department ID"
FIMAN = "Financial Manager"


class COA(SourceData):
    def __init__(self, coa_data: list[dict]):
        super(COA, self).__init__(coa_data)

    def find_fiman(self, department_id: str):
        return self.find(FIMAN, DEPT_ID, department_id)

    def find_all_fiman_dept(self, financial_manager: str):
        return self.findall(DEPT_ID, FIMAN, financial_manager)
