#! /usr/bin/python3.7.6


class DataRow(object):
    def __init__(self, header, row_data, index=0, parent=None):
        self._header = header
        self._data = list(row_data)
        self._index = index
        self._parent = parent

    @property
    def data(self):
        """
        Returns row data as a list.

        """
        return self._data

    @property
    def index(self):
        return self._index

    @property
    def parent(self):
        return self._parent

    def header(self):
        """
        Returns row header as a list.

        """
        return self._header

    def as_dict(self):
        row_data = zip(self.header(), self.data)
        return dict(row_data)

    def get(self, key):
        """Returns the value for a given key

        """
        try:
            return self[key]
        except KeyError:
            return None

    def attributes(self):
        width = max(len(header) for header in ["Index", "Parent"] + self.header()) + 2

        print("___DataRow___\n{:<{w}}{}\n{:<{w}}{}".format("Index:", self.index,
                                                           "Parent:", self.parent,
                                                           w=width))

        for header, data in list(zip(self.header(), self.data)):
            print("{:<{w}}{}".format(header + ":", data, w=width))

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, header):
        # get item --> index-based
        if isinstance(header, int):
            return self.data[header]

        # get item --> string-based
        if header in self.header():
            i = self.header().index(header)
            if self.header().count(header) > 1:
                raise KeyError("DataRow has multiple header={}.".format(header))
            return self.data[i]

        raise KeyError("DataRow has no header={}.".format(header))

    def __repr__(self):
        return "DataRow(index={})".format(self.index)
