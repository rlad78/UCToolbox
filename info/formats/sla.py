from .sourcedata import SourceData, Entry
from typing import Union

# CSV HEADER LABELS
NAME = 'BUILDING'
SLA_NBR = 'SLA NBR'
ADDRESS = '911 ADDRESS'
BLDG_ID = 'BUILDING ID'


class SLAEntry(Entry):
    def __init__(self, sla_entry: dict):
        super(SLAEntry, self).__init__(sla_entry)
        self.building = sla_entry[NAME]
        self.sla = sla_entry[SLA_NBR]
        self.address = sla_entry[ADDRESS]
        self.bldg_id = sla_entry[BLDG_ID]
        if self.building == '':
            self.building = "SLA " + self.sla


class SLA(SourceData):
    def __init__(self, sla_data: list[dict]):
        super(SLA, self).__init__(sla_data)

    def get_bldg_name(self, sla_number='', building_id='') -> str:
        if sla_number:
            return self._find(NAME, SLA_NBR, sla_number)
        elif building_id:
            return self._find(NAME, BLDG_ID, building_id)
        else:
            print('[SLA.get_bldg_name] tried to search with blank search values')
            return ''

    def get_building_sla(self, building_id: str) -> str:
        return self._find(SLA_NBR, BLDG_ID, building_id)

    def get_building_id(self, sla_number: str) -> str:
        return self._find(BLDG_ID, SLA_NBR, sla_number)

    def get_building(self, sla_number='', building_id='') -> Union[SLAEntry, None]:
        if building_id:
            this_building = self._get(BLDG_ID, building_id)
            if not this_building and sla_number:
                this_building = self._get(SLA_NBR, sla_number)
        elif sla_number:
            this_building = self._get(SLA_NBR, sla_number)
        else:
            raise Exception('[SLA.get_building] tried to get building with no criteria')

        if this_building:
            return SLAEntry(this_building)
        else:
            return None

    def get_locations(self, loc_pairs: list[tuple[str, str]]) -> list[dict]:
        loc_flat: dict[str, SLAEntry] = {}
        for sla_num, bldg_id in loc_pairs:
            if sla_num not in loc_flat:
                loc = self.get_building(sla_number=sla_num)
                if loc is not None:
                    loc_flat[sla_num] = loc
            elif bldg_id not in loc_flat[sla_num][BLDG_ID].split(', ') and bldg_id != '':
                loc_flat[sla_num].data[BLDG_ID] = ', '.join(loc_flat[sla_num][BLDG_ID].split(', ') + [bldg_id])
        return [d.data for d in loc_flat.values()]
