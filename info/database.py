class Database:
    def __init__(self, db: list[dict]):
        self.data = db
        self._categories = [s for s in self.data[0].keys()]

    def __iter__(self):
        for line in self.data:
            yield line

    def __getitem__(self, item):
        if item not in self._categories:
            raise Exception(f'[Database]: "{item}" not a valid line category')
        return self.data[item]


