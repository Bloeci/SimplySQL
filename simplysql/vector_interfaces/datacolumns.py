#! /usr/bin/python3.7.6

from simplysql.vector_interfaces.datacolumn import DataColumn


class DataColumns(object):
    def __init__(self, names, columns, parent):
        self._names = names
        self._columns = list(map(list, zip(*columns)))
        self._parent = parent

    @property
    def data(self):
        return self._columns

    @property
    def parent(self):
        return self._parent

    def names(self):
        """
        Returns the list of column within the row.

        """
        return self._names

    def all(self):
        return self._columns

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    def count(self):
        return len(self._columns)

    def __len__(self):
        return len(self._columns)

    def __iter__(self):
        i = 0

        while True:
            if i < self.count():
                yield self[i]
            else:
                return
            i += 1

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index

            return DataColumn(self.names()[index], self.all()[index],
                              index, self.parent)

        raise IndexError("DataColumns has no index={}.".format(index))

    def __repr__(self):
        return "DataColumns(count={})".format(len(self))
