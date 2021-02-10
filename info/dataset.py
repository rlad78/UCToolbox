from .formats import *


class Dataset:
    def __init__(self, data_members: dict):
        try:
            self.att = ATT(data_members['ATT'])
        except KeyError as e:
            raise Exception(f'[Dataset] missing data member {e.args[0]}')
