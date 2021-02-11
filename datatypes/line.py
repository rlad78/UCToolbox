import re


class Line:
    def __init__(self, directory_number: str, dataset: dict):
        self._categories: list[str] = [
            "Phone Number", "User ID", "Name", "Department", "Dept. Code", "Financial Manager", "Building", "Floor",
            "Room", "Business Set?", "Forward All", "Line Appearances", "Busy Lamp Fields", "Call Pickup Group",
            "Customer Notes", "UC Notes", "GL String", "Device Model", "Phone Name", "line_type", "bldg_id", "sla_nbr",
            'mysoft_name', 'hr_full_name'
        ]

        self.info: dict = {
            k: '' for k in self._categories
        }
        self.info['Phone Number'] = directory_number
        self.dn = directory_number

    def update(self, new_info: dict) -> None:
        for key in new_info:
            if key not in self._categories:
                raise Exception(f'[Line] tried to enter a non-standard category "{key}"')
        self.info.update(new_info)
