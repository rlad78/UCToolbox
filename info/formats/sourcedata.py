class SourceData:
    def __init__(self, source: list[dict]):
        if source is None or not source:
            raise Exception(f'No data entered for {self.__class__.__name__}!')
        self._data = source

    def __iter__(self):
        for entry in self._data:
            yield entry
