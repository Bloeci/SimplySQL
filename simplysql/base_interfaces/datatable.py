#! /usr/bin/python3.7.6

from simplysql.vector_interfaces.datarows import DataRows
from simplysql.vector_interfaces.datarow import DataRow
from simplysql.vector_interfaces.datacolumns import DataColumns
from simplysql.vector_interfaces.datacolumn import DataColumn


class DataTable(object):
    def __init__(self, parent=None, id=0, name=None, header=None, htypes=None, exists=False):
        self._rowid = None
        self._id = id
        self._name = name
        self._header = header
        self._htypes = htypes
        self._parent = parent

        if not exists:
            self._create()

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._id

    @property
    def empty(self):
        if self.count_rows() >= 1:
            return False
        return True

    @property
    def max_row(self):
        return self.count_rows()

    @property
    def max_column(self):
        return self.count_columns()

    @property
    def shape(self):
        return (self.max_row, self.max_column)

    @property
    def exists(self):
        return self._exists

    @property
    def parent(self):
        return self._parent

    @property
    def data(self):
        return [tuple(list(row)[1:]) for row in self._get_table()]

    @property
    def rowids(self):
        return [row[0] for row in self._get_table()]

    def header(self):
        return self._header

    def htypes(self):
        return self._htypes

    def count_rows(self):
        return len(self.data)

    def count_columns(self):
        return len(self.header())

    def as_table(self, with_rowid=False):
        return self._to_string(with_rowid=with_rowid)

    def as_dict(self):
        return dict(zip(self.header(), list(map(list, zip(*self.data)))))

    def as_list(self):
        return list(map(list, self.data))

    def as_tuple(self):
        return tuple(self.data)

    def rename_column(self, old_name, new_name):
        """
        Short summary.

        Args:
            old_name (type): Description of parameter `old_name`.
            new_name (type): Description of parameter `new_name`.
        """
        if old_name not in self.header():
            raise ValueError(f"DataTable has no column named {old_name}")

        sql = "ALTER TABLE {} RENAME COLUMN {} TO {}".format(self.name, old_name, new_name)
        self.parent.query(sql)
        self.parent._rename_table_column(self.index, old_name, new_name)

    def columns(self):
        return DataColumns(self.header(), list(self.data), self)

    def column(self, index):
        if not isinstance(index, int):
            index = self.header().index(index)

        if not abs(index) <= self.count_columns():
            raise IndexError(f"DataTable has no column index {index}")

        column = [row[index] for row in self.data]

        return DataColumn(self.header()[index], column,
                          index=index, parent=self)

    def rows(self):
        return DataRows(self.header(), list(self.data), self)

    def row(self, index):
        if not abs(index) <= self.count_rows():
            raise IndexError(f"DataTable has no row index {index}")

        if index < 0:
            index = self.max_row + index

        row = list(self.data[index])

        return DataRow(self.header(), row, index=index, parent=self)

    def insert_row(self, row_data):
        if len(row_data) != self.count_columns():
            raise IndexError("Number of data ({}) out of range".format(
                len(row_data)))

        sql = "INSERT INTO {} VALUES {}".format(self.name, tuple(row_data))
        self.parent.query(sql)

    def insert_rows(self, rows_data):
        for row_data in rows_data:
            self.insert_row(row_data)

    def delete_row(self, index):
        if index < 0:
            index = self.max_row + index

        rowid = self.rowids[index]

        sql = "DELETE FROM {} WHERE rowid={}".format(self.name, rowid)
        self.parent.query(sql)

    def delete_rows(self, indexes):
        for index in indexes:
            self.delete_row(index)

    def delete_table(self):
        sql = "DELETE FROM {}".format(self.name)
        self.parent.query(sql)

    def delete_where(self, deleting_items):
        sql = "DELETE FROM {} WHERE ".format(self.name)

        for item in deleting_items:
            column, value = item

            if isinstance(value, str):
                sql += "{}='{}'".format(column, value)
            elif isinstance(value, int):
                sql += "{}={}".format(column, value)

            if item != deleting_items[-1]:
                sql += " AND "

        self.parent.query(sql)

    def _create(self):
        cols = [str(col) + " " + type for col, type in zip(self.header(), self.htypes())]
        joined_cols = ", ".join(cols)
        sql = "CREATE TABLE {}({})".format(self._name, joined_cols)
        self.parent.query(sql)

    def head(self, max_rows=5, with_rowid=False):
        return self._to_string(with_rowid, max_rows)

    def attributes(self):
        print(f"___DataTable___\n"
              f"Name:               {self.name}\n"
              f"Parent:             {self.parent}\n"
              f"Index:              {self.index}\n"
              f"Empty:              {self.empty}\n"
              f"Shape:              {self.shape}\n"
              f"Columns:            {self.header()}\n"
              f"Column data types:  {self.htypes()}\n"
              f"Number of columns:  {self.count_columns()}\n"
              f"Number of rows:     {self.count_rows()}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return "DataTable(name={})".format(self.name)

    def _get_table(self):
        sql = "SELECT rowid, * FROM {}".format(self.name)
        # self.parent.query(sql)

        return self.parent.query(sql)
        # return self.parent.fetchall()

    def _to_string(self, with_rowid=False, max_rows=None):
        result = []

        max = self.count_rows()
        if max_rows is None or max_rows > max:
            max_rows = max

        column_width = self._width([self.header()] + self.data)

        if with_rowid:
            column_width.insert(0, len("rowid") + 1)

        fmt_row = "".join("{{:<{w}}}".format(w=width + 1) for width in column_width)
        fmt_row = "{{:<{w}}}".format(w=len(str(self.max_row)) + 1) + fmt_row

        header = ["", "rowid"] + self.header() if with_rowid else [""] + self.header()
        data = list(self._get_table()) if with_rowid else self.data

        result += [fmt_row.format(*header)]
        result += [fmt_row.format(row, *line)
                   for row, line in enumerate(data) if row < max_rows]

        return str("\n".join(result))

    def _width(self, table):
        transpo_table = [list(x) for x in zip(*table)]
        return [self._column_width(col) for col in transpo_table]

    def _column_width(self, column):
        return max(len(str(row)) for row in column)
