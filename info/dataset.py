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
