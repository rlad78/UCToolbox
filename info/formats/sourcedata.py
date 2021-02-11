import re


class SourceData:
    def __init__(self, source: list[dict]):
        if source is None or not source:
            raise Exception(f'No data entered for {self.__class__.__name__}!')
        self._data = source
        self._categories = [x for x in self._data[0].keys()]

    def __iter__(self):
        for entry in self._data:
            yield entry

    def _get(self, category: str, value: str) -> dict:
        """
        Returns first found entry that matches the value in the specified category.

        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param value: String to search against.
        :return: The dict (entry) satisfying the category value constraint. Returns an empty dict {} if no
                 matching entry is found.
        """

        self.__check_category(category)
        for entry in self._data:
            if entry[category] == value:
                return entry
        else:
            return {}

    def _getall(self, category: str, value: str) -> list[dict]:
        """
        Same functionality as self.get(), but returns all matching entries in a list.
        :param category: Any str value matching a category in the csv header. Method will raise exception if

                         category is not within the csv header.
        :param value: String to search against.
        :return: A dict-list of all entries satisfying the category value constraint. Returns an empty list [] if no
                 matching entry is found.
        """
        self.__check_category(category)
        matching_entries: list[dict] = []
        for entry in self._data:
            if entry[category] == value:
                matching_entries.append(entry)
        return matching_entries

    def _find(self, wanted: str, category: str, value: str) -> str:
        """
        Uses self.get() to find the first entry matching the category value condition, then returns that entries'
        wanted category data.

        :param wanted: Any str value matching a category in the csv header. Method will raise exception if
                       category is not within the csv header.
        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param value: String to search against.
        :return: String of wanted data. Will return '' if a matching entry is not found.
        """
        self.__check_category(wanted, category)
        try:
            return self._get(category, value)[wanted]
        except KeyError:
            return ''

    def _findall(self, wanted: str, category: str, value: str) -> list[str]:
        """
        Same functionality as self.find(), but uses self.getall() to get a list of all matching entries.
        Returns the wanted data for all entries found.

        :param wanted: Any str value matching a category in the csv header. Method will raise exception if
                       category is not within the csv header.
        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param value: String to search against.
        :return: String-list of wanted data. Will return empty list [] if no matching entries are found.
        """
        self.__check_category(wanted, category)
        entries: list[dict] = self._getall(category, value)
        if not entries:
            return []
        else:
            return [d[wanted] for d in entries]

    def _query(self, required_matches: dict) -> list[dict]:
        """
        Finds entries that match all key-value pairs in required_matches. Returns empty list [] if none found.

        :param required_matches: A dict whose keys all match a category in the csv header
        :return: List of all matching entries. Empty list if no entries found.
        """
        self.__check_category(*list(required_matches.keys()))
        matching_entries: list[dict] = []
        for entry in self._data:
            for key, value in required_matches.items():
                if entry[key] == value:
                    continue  # if the value matches, keep checking the rest
                else:
                    break  # if one of the values doesn't match, escape and go on to next entry
            else:
                matching_entries.append(entry)  # add entry to the matching list if all of the values matched
        return matching_entries

    def _parse(self, category: str, regex: str) -> dict:
        """
        Same functionality as self.get(), but uses regex matching instead of str matching.

        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param regex: Any regular expression except for ''. self.parse() will automatically return empty
                      dict {} if blank regex is provided.
        :return: The dict (entry) satisfying the regex constraint. Returns an empty dict {} if no
                 matching entry is found.
        """
        searcher = re.compile(regex, re.IGNORECASE)
        for entry in self._data:
            if re.search(searcher, entry[category]):
                return entry
        else:
            return {}

    def _parseall(self, category: str, regex: str) -> list[dict]:
        """
        Same functionality as self.getall(), but uses regex matching instead of str matching.

        :param category: Any str value matching a category in the csv header. Method will raise exception if
                         category is not within the csv header.
        :param regex: Any regular expression except for ''. self.parse() will automatically return empty
                      dict {} if blank regex is provided.
        :return: List of entries satisfying the regex constraint. Returns an empty list [] if no
                 matching entry is found.
        """
        searcher = re.compile(regex, re.IGNORECASE)
        matching_entries: list[dict] = []
        for entry in self._data:
            if re.search(searcher, entry[category]):
                matching_entries.append(entry)
        return matching_entries

    def __check_category(self, *args):
        """
        Checks that each argument exists as a category in the csv header.

        :param args: Any strings
        :type args: str
        :return: None
        """
        for category in args:
            if category not in self._categories:
                raise Exception(f'{category} is not a valid category for {self.__class__.__name__}\n{self._categories}')

    def _format_phone_numbers(self, *categories) -> None:
        for category in categories:
            for entry in self._data:
                if not entry[category].isnumeric():
                    entry[category] = format_dn(entry[category])


class Entry:
    def __init__(self, data: dict):
        self.data = data

    def __getitem__(self, item):
        try:
            return self.data[item]
        except KeyError:
            raise KeyError(f'{self.__class__.__name__} does not contain "{item}" value')

    def __iter__(self):
        for key, value in self.data.items():
            yield key, value

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()


def format_dn(number: str) -> str:
    digits = ''
    for c in number:
        if c.isnumeric():
            digits += c
    if len(digits) == 10:
        return digits
    elif len(digits) == 12 and digits[:2] == '91':
        return digits[2:]
    elif len(digits) == 8 and digits[:1] == '9':
        return '864' + digits[1:]
    elif len(digits) == 7 and digits[:3] == '656':
        return '864' + digits
    else:
        return ''
