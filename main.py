from actions import data, write
from datatypes import Line


def search_line_demo(phone_number: str) -> Line:
    dataset = data.load_dataset()
    me = Line(phone_number)
    me.update(dataset.get_line_all(phone_number))
    return me


if __name__ == '__main__':
    write.write_buildings(data.load_dataset())
