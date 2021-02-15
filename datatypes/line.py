class Line:
    def __init__(self, directory_number: str, info=None):
        self._categories: list[str] = [
            "Phone Number", "User ID", "Name", "Department", "Dept. Code", "Financial Manager", "Building", "Floor",
            "Room", "Business Set?", "Forward All", "Line Appearances", "Busy Lamp Fields", "Call Pickup Group",
            "Customer Notes", "UC Notes", "GL String", "Device Model", "Phone Name", "line_type", "bldg_id", "sla_nbr",
            'mysoft_name', 'hr_full_name'
        ]

        if info is not None and type(info) == dict:
            self.info: dict = {}
            self.info.update(info)
        else:
            self.info: dict = {
                k: '' for k in self._categories
            }
        self.info['Phone Number'] = directory_number
        self.dn = directory_number

    def __str__(self):
        spacer = ' ' * 14  # '[864656XXXX]: '
        char_width = 120
        title: dict = {
            'Phone Number': self.info["Phone Number"],
            'Name': self.info["Name"],
            'Building': self.info["Building"],
            'Room': self.info['Room'],
            'sla_nbr': self.info["sla_nbr"],
            'line_type': self.info["line_type"]
        }
        out: str = f'[{title["Phone Number"]}]: <{title["line_type"]}> '
        out += f'"{title["Name"]}" in {title["Building"]} {title["Room"]} (SLA {title["sla_nbr"]})'
        out += '\n' + spacer

        total_print = 0
        for key, value in {k: v for k, v in self.info.items() if k not in title.keys() and v != ''}.items():
            if total_print + len(key) + len(value) + 6 > char_width:
                out += '\n' + spacer
                total_print = 0
            add_to_out = f'[{key}]: {value}  '
            total_print += len(add_to_out)
            out += add_to_out
        return out

    def __iter__(self):
        for k, v in self.info.items():
            yield k, v

    def __getitem__(self, item):
        return self.info[item]

    def update(self, new_info: dict) -> None:
        for key in new_info:
            if key not in self._categories:
                raise Exception(f'[Line] tried to enter a non-standard category "{key}"')
        self.info.update(new_info)
