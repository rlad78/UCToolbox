from .sourcedata import SourceData


# CSV HEADER LABELS
DN = 'Telephone Number'
BUSY_FORWARD = 'CFBTN'
NO_ANSWER_FORWARD = 'CFDTN'


class CFD(SourceData):
    def __init__(self, cfd_data: list[dict]):
        super(CFD, self).__init__(cfd_data)
        self._format_phone_numbers(DN, NO_ANSWER_FORWARD)

    def get_forwarding(self, phone_number: str) -> str:
        return self._find(NO_ANSWER_FORWARD, DN, phone_number)
