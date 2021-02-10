class SourceData:
    def __init__(self, source: list[dict]):
        if source is None or not source:
            raise Exception(f'No data entered for {self.__class__.__name__}!')
        self._data = source
        self._categories = [x for x in self._data[0].keys()]

    def __iter__(self):
        for entry in self._data:
            yield entry

    def get(self, category: str, value: str) -> dict:
        """
        Returns first found entry that matches the value in the specified category
        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param value: String to search against.
        :return: The dict (entry) satisfying the category value constraint. Returns an empty dict {} if no
                 matching entry is found.
        """

        if category not in self._categories:
            raise Exception(f'{category} is not a valid category for {self.__class__.__name__}\n{self._categories}')
        for entry in self._data:
            if entry[category] == value:
                return entry
        else:
            return {}

    def getall(self, category: str, value: str) -> list[dict]:
        """
        Same functionality as self.get(), but returns all matching entries in a list
        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param value: String to search against.
        :return: A dict-list of all entries satisfying the category value constraint. Returns an empty list [] if no
                 matching entry is found.
        """
        pass

    def find(self, wanted_category: str, category: str, value: str) -> str:
        pass

    def findall(self, wanted_category: str, category: str, value: str) -> list[str]:
        pass

    def query(self, required_matches: dict) -> list[dict]:
        pass
