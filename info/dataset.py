from .formats import *
from datatypes import Location


class Dataset:
    """
    This should be used for BUILDING THE DATABASE ONLY!!
    All other searching should be done in database.py
    """
    def __init__(self, data_members: dict):
        try:
            self.att = ATT(data_members['ATT'])
            self.coa = COA(data_members['COA'])
            self.hr = HR(data_members['HR'])
            self.mysoft = MYSOFT(data_members['MYSOFT'])
            self.sla = SLA(data_members['SLA'])
            self.voip = VOIP(data_members['VOIP'])

            self.blf = BLF(data_members['BLF'])
            self.bset = BSET(data_members['BSET'])
            self.cfd = CFD(data_members['CFD'])
            self.cpg = CPG(data_members['CPG'])
            self.la = LA(data_members['LA'])
        except KeyError as e:
            raise Exception(f'[Dataset] missing data member {e.args[0]}')

    def get_att_numbers(self) -> list[str]:
        return self.att.list_all_lines()

    def get_line_info(self, phone_number: str) -> dict:
        line_info: dict = {
            'Phone Number': phone_number,
        }
        att_info: ATTEntry = self.att.get_line(phone_number)
        if att_info is None:
            return line_info
        else:
            line_info['line_type'] = att_info.line_type
            line_info['bldg_id'] = att_info.bldg_code
            line_info['Floor'] = att_info.floor
            line_info['Room'] = att_info.room
            line_info['sla_nbr'] = att_info.sla
            line_info['Building'] = self.sla.get_bldg_name(sla_number=att_info.sla, building_id=att_info.bldg_code)
            return line_info

    def get_voip_info(self, phone_number: str) -> dict:
        voip_info: VOIPEntry = self.voip.get_phone(phone_number)
        if voip_info is None:
            return {}
        else:
            return {
                'User ID': voip_info.user_id,
                'Name': voip_info.description,
                'Device Model': '',  # TODO: get method for finding device model
                'Phone Name': voip_info.device_name
            }

    def get_dept_info(self, phone_number: str) -> dict:
        line_info: dict = {}
        mysoft_info: MYSOFTEntry = self.mysoft.get_line(phone_number)
        if mysoft_info is None:
            return {}
        else:
            line_info.update({
                'Dept. Code': mysoft_info.dept,
                'GL String': mysoft_info.gl
            })
            coa_info: COAEntry = self.coa.get_dept(mysoft_info.dept)
            if coa_info is None:
                return line_info
            else:
                line_info.update({
                    'Department': coa_info.department,
                    'Financial Manager': coa_info.financial_manager
                })
                return line_info

    def get_centrex_ownership(self, phone_number: str) -> dict:
        mysoft_info: MYSOFTEntry = self.mysoft.get_line(phone_number)
        if mysoft_info is None:
            return {}

        guess_name = mysoft_info.name
        guess_dept = mysoft_info.dept

        real_user: HREntry = self.hr.find_user(phone_number, dept_num=guess_dept, guess_name=guess_name)
        if real_user is None:
            return {
                'Name': mysoft_info.name,
                'Dept. Code': mysoft_info.dept
            }
        else:
            return {
                'Name': real_user.shortname,
                'User ID': real_user.user_id,
                'Dept. Code': real_user.dept_id,
                'mysoft_name': guess_name,
                'hr_full_name': real_user.name
            }

    def get_centrex_cxm(self, phone_number: str) -> dict:
        return {
            'Business Set?': 'Yes' if self.bset.is_bset(phone_number) else '',
            'Forward All': self.cfd.get_forwarding(phone_number),
            'Line Appearances': ', '.join(self.la.get_las(phone_number)),
            'Busy Lamp Fields': ', '.join(self.blf.get_blfs(phone_number)),
            'Call Pickup Group': ', '.join(self.cpg.get_cpg_lines(phone_number)),
        }

    def get_location_info(self, building_id='', sla_num='') -> dict:
        if not building_id and not sla_num:
            return {}
        this_location: SLAEntry = self.sla.get_building(building_id, sla_num)
        if this_location is None:
            return {}
        else:
            return {
                "Name": this_location.building,
                "Address": this_location.address,
                "SLA": this_location.sla,
                'Building ID': this_location.bldg_id
            }

    def get_all_locations(self) -> list[Location]:
        loc_flat: dict[str, dict] = {}
        for entry in self.sla:
            pass  # TODO: go through each element and add loc_flat[SLA]

    def get_line_all(self, phone_number: str) -> dict:
        line_info: dict = {'Phone Number': phone_number}
        line_info.update(self.get_line_info(phone_number))
        line_info.update(self.get_dept_info(phone_number))
        if line_info['line_type'] == 'VOIP':
            line_info.update(self.get_voip_info(phone_number))
        else:
            line_info.update(self.get_centrex_cxm(phone_number))
            line_info.update(self.get_centrex_ownership(phone_number))
        return line_info
