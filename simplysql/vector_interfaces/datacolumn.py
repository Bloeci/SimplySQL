#! /usr/bin/python3.7.6
from typing import Tulpe, List, Dict, Any


class DataColumn(object):
    def __init__(self, name: str, values: List[Any], index: int = 0, parent=None):
        self._name = name
        self._values = values
        self._index = index
        self._parent = parent

    @property
    def index(self) -> int:
        return self._index

    @property
    def parent(self):
        return self._parent

    def name(self) -> str:
        """
        Returns the column name

        """
        return self._name

    def values(self) -> List[Any]:
        """
        Returns the list of values

        """
        return self._values

    @property
    def data(self) -> Dict():
        return dict([(self.name(), self.values())])

    def get(self, name):
        """
        Returns the value for a given column name

        """
        try:
            return self[name]
        except KeyError:
            return None

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, name):
        # get item --> index-based
        if isinstance(name, int):
            return self.values()[name]

        # get item --> string-based
        if name in self.name():
            i = self.name().index(name)
            if self.name().count(name) > 1:
                raise KeyError("DataColumn has multiple keys={}.".format(name))
            return self.values()[i]

        raise KeyError("DataColumn has no name={}.".format(name))

    def __repr__(self):
        return "DataColumn(index={})".format(self.index)
