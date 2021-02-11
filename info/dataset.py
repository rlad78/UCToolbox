from .formats import *


class Dataset:
    def __init__(self, data_members: dict):
        try:
            self.att = ATT(data_members['ATT'])
            self.coa = COA(data_members['COA'])
            self.hr = HR(data_members['HR'])
            self.mysoft = MYSOFT(data_members['MYSOFT'])
            self.sla = SLA(data_members['SLA'])
            self.voip = VOIP(data_members['VOIP'])
        except KeyError as e:
            raise Exception(f'[Dataset] missing data member {e.args[0]}')

    def get_line_info(self, phone_number: str) -> dict:
        line_info: dict = {
            'Phone Number': phone_number,
            'bldg_id': '',
            'Floor': '',
            'Room': '',
            'sla_nbr': ''
        }
        att_info: ATTEntry = self.att.get_line(phone_number)
        if att_info is None:
            return line_info
        else:
            line_info['bldg_id'] = att_info.bldg_code
            line_info['Floor'] = att_info.floor
            line_info['Room'] = att_info.room
            line_info['sla_nbr'] = att_info.sla
            return line_info
