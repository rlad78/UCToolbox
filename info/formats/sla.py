from .sourcedata import SourceData


class SLA(SourceData):
    # CSV HEADER LABELS
    NAME = 'BUILDING'
    SLA_NBR = 'SLA NBR'
    ADDRESS = '911 ADDRESS'
    BLDG_ID = 'BUILDING ID'

    def __init__(self, sla_data: list[dict]):
        super(SLA, self).__init__(sla_data)

    def get_bldg_name(self, sla_number='', building_id='') -> str:
        if sla_number:
            return self._find(self.NAME, self.SLA_NBR, sla_number)
        elif building_id:
            return self._find(self.NAME, self.BLDG_ID, building_id)
        else:
            print('[SLA.get_bldg_name] tried to search with blank search values')
            return ''

    def get_building_sla(self, building_id: str) -> str:
        return self._find(self.SLA_NBR, self.BLDG_ID, building_id)

    def get_building_id(self, sla_number: str) -> str:
        return self._find(self.BLDG_ID, self.SLA_NBR, sla_number)
