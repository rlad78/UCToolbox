from .formats import *
from datatypes import Line
import re


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
            self.fiber = FIBER(data_members['FIBER'])
        except KeyError as e:
            raise Exception(f'[Dataset] missing data member {e.args[0]}')

    def get_att_numbers(self) -> list[str]:
        return self.att.list_all_lines()

    def get_line_info(self, line: Line) -> None:
        # line_info: dict = {
        #     'Phone Number': line["Phone Number"],
        # }
        line_info: dict = {}
        att_info: ATTEntry = self.att.get_line(line["Phone Number"])
        if att_info is None:
            return None
        else:
            line_info['line_type'] = att_info.line_type
            line_info['bldg_id'] = att_info.bldg_code
            line_info['Floor'] = att_info.floor
            line_info['Room'] = att_info.room
            line_info['sla_nbr'] = att_info.sla
            line_info['Building'] = self.sla.get_bldg_name(sla_number=att_info.sla, building_id=att_info.bldg_code)
            line.update(line_info)

    def get_voip_info(self, line: Line) -> None:
        voip_info: VOIPEntry = self.voip.get_phone(line['Phone Number'])
        if voip_info is None:
            return {}
        else:
            line.update({
                'User ID': voip_info.user_id,
                'Name': voip_info.description,
                'Device Model': '',  # TODO: get method for finding device model
                'Phone Name': voip_info.device_name
            })

    def get_dept_info(self, line: Line) -> None:
        line_info: dict = {}
        mysoft_info: MYSOFTEntry = self.mysoft.get_line(line['Phone Number'])
        if mysoft_info is not None:
            line.update({
                'Dept. Code': mysoft_info.dept,
                'GL String': mysoft_info.gl
            })
            coa_info: COAEntry = self.coa.get_dept(mysoft_info.dept)
            if coa_info is not None:
                line.update({
                    'Department': coa_info.department,
                    'Financial Manager': coa_info.financial_manager
                })

    def get_centrex_ownership(self, line: Line) -> None:
        mysoft_info: MYSOFTEntry = self.mysoft.get_line(line['Phone Number'])
        if mysoft_info is None:
            return None

        guess_name = mysoft_info.name
        guess_dept = mysoft_info.dept

        real_user: HREntry = self.hr.find_user(line['Phone Number'], dept_num=guess_dept, guess_name=guess_name)
        if real_user is None:
            line.update({
                'Name': mysoft_info.name,
                'Dept. Code': mysoft_info.dept
            })
        else:
            line.update({
                'Name': real_user.shortname,
                'User ID': real_user.user_id,
                'Dept. Code': real_user.dept_id,
                'mysoft_name': guess_name,
                'hr_full_name': real_user.name
            })

    def get_centrex_cxm(self, line: Line) -> None:
        line.update({
            'Business Set?': 'Yes' if self.bset.is_bset(line['Phone Number']) else '',
            'Forward All': self.cfd.get_forwarding(line['Phone Number']),
            'Line Appearances': ', '.join(self.la.get_las(line['Phone Number'])),
            'Busy Lamp Fields': ', '.join(self.blf.get_blfs(line['Phone Number'])),
            'Call Pickup Group': ', '.join(self.cpg.get_cpg_lines(line['Phone Number'])),
        })

    def get_emg_type(self, line: Line) -> None:
        line_name = line.get('Name')
        line_rm = line.get('Room')
        line_bldg = line.get('Building')

        s_fire_name = re.compile(r'(fire|facp)', re.I)
        s_fire_room = re.compile(r'(fire|alarm|alrm)', re.I)
        s_elev_name = re.compile(r'(elev|elv)', re.I)
        s_elev_room = re.compile(r'(ele|elv)', re.I)
        s_emrg_bldg = re.compile(r'(EM\s*PH|EP\s|EP\w{3,4}|EMER.*PHONE)', re.I)

        if re.search(s_fire_name, line_name) or re.search(s_fire_room, line_rm):
            if self.fiber.check_fiber_facp(line_bldg):
                line.update({
                    "UC Notes": "Fire Alarm on fiber. Disconnect/reuse this line.",
                    "emg_type": "fiber"
                })
            else:
                line.update({
                    "UC Notes": "Fire alarm dialer, most likely not on fiber.",
                    "emg_type": "fire"
                })
        elif re.search(s_elev_name, line_name) or re.search(s_elev_room, line_rm):
            line.update({
                "UC Notes": "Elevator phone line. Ensure building has UPS before port.",
                "emg_type": "elevator"
            })
        elif re.search(s_emrg_bldg, line_bldg):
            line.update({
                "UC Notes": 'Blue-light/emergency phone line.',
                "emg_type": "emergency"
            })

    def get_line_all(self, line: Line) -> None:
        self.get_line_info(line)
        self.get_dept_info(line)
        if line.get('line_type') == 'VOIP':
            self.get_voip_info(line)
        else:
            self.get_centrex_cxm(line)
            self.get_centrex_ownership(line)
        self.get_emg_type(line)

    #########################################
    ### F O R   L O C A T I O N   I N F O ###
    #########################################
    
    def get_location_info(self, building_id='', sla_num='') -> dict:
        if not building_id and not sla_num:
            return {}
        this_location: SLAEntry = self.sla.get_building(sla_num, building_id)
        if this_location is None:
            return {}
        else:
            return {
                "Name": this_location.building,
                "Address": this_location.address,
                "SLA": this_location.sla,
                'Building ID': this_location.bldg_id
            }

    def get_all_locations(self) -> list[dict]:
        return self.sla.get_locations(self.att.list_all_loc())
