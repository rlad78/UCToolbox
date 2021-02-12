from .formats import SourceData


class Database(SourceData):
    def __init__(self, db: list[dict]):
        super(Database, self).__init__(db)

    def query(self, required_matches: dict):
        super(Database, self)._query(required_matches)

