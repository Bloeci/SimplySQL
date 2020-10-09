#! /usr/bin/python3.7.6

from simplysql.vector_interfaces.datarow import DataRow


class DataRows(object):
    def __init__(self, header, rows, parent):
        self._header = header
        self._rows = rows
        self._parent = parent

    @property
    def data(self):
        return self._rows

    @property
    def parent(self):
        return self._parent

    def header(self):
        """
        Returns the list of column within the row.

        """
        return self._header

    def all(self):
        return self._rows

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    def count(self):
        return len(self._rows)

    def __len__(self):
        return len(self._rows)

    def __repr__(self):
        return "DataRows(count={})".format(len(self))

    def __iter__(self):
        index = 0

        while True:
            if index < self.count():
                yield self[index]
            else:
                return
            index += 1

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index

            return DataRow(self.header(), self.all()[index],
                           index, self.parent)

        raise IndexError("DataRows has no index={}.".format(index))
