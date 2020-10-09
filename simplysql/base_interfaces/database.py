#! /usr/bin/python3.7.6

# import sqlite3
from pathlib import Path

from simplysql.base_interfaces.datatable import DataTable
from simplysql.conn_interfaces.connection import Connection


class DataBase(object):
    def __init__(self, path=None):

        if not path:
            raise ValueError("You must provide a path.")

        self._path = Path(path)
        self._filename = self._path.stem
        self._filetype = self._path.suffix.split(".")[1]
        self._database = self._path.name
        self.open = True

        self._tables = {}

        self._get_all_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_connection(self):
        """
        Get a connection to this Database.

        """

        return Connection(self._path)

    @property
    def name(self):
        return self._database

    def close(self):
        self.open = False

    def query(self, sql, params=None):
        with self.get_connection() as conn:
            conn.execute(sql, params or ())
            return conn.fetchall()

    def create_table(self, table_name, columns, datatypes):
        if not self.has_table(table_name):
            table_id = self.count_tables() + 1
            table = DataTable(self, table_id, table_name, columns, datatypes, False)

            self._tables[table_id] = {"table": table,
                                      "name": table.name,
                                      "columns": table.header(),
                                      "datatypes": table.htypes()}

    def count_tables(self):
        return len(self._tables)

    def has_tables(self):
        return True if self.count_tables() > 0 else False

    def get_tablenames(self):
        return [table["name"] for table in self._tables.values()]

    def has_table(self, table):
        return True if table in self.get_tablenames() else False

    def table(self, index):
        return self._tables[index]["table"]

    def first_table(self):
        if self.has_tables():
            return self._tables[1]["table"]

    def last_table(self):
        if not self.has_tables():
            raise ValueError("DataBase has no tables")

        if self.count_tables() > 1:
            return self._tables[self.count_tables()]["table"]

        return self.first_table()

    def attributes(self):
        print(f"___DataBase___\n"
              f"Name:               {self.name}\n"
              f"Filetype:           {self._filetype}\n"
              f"Path:               {self._path}\n"
              f"Has tables:         {self.has_tables()}\n"
              f"Number of tables:   {self.count_tables()}\n")

    def _get_all_tables(self):

        with self.get_connection() as conn:
            sql = "SELECT * FROM sqlite_master WHERE type='table'"

            for tables in conn.query(sql):
                sql = "PRAGMA TABLE_INFO({})".format(tables[1])
                table_info = conn.query(sql)

                columns = [table[1] for table in table_info]
                datatypes = [table[2] for table in table_info]

                table_id = self.count_tables() + 1
                table_name = tables[1]

                table = DataTable(self, table_id, table_name, columns, datatypes, True)

                self._tables[table_id] = {"table": table,
                                          "name": table.name,
                                          "columns": table.header(),
                                          "datatypes": table.htypes()}

    def _rename_table_column(self, table_id, old_name, new_name):
        columns = self._tables[table_id]["columns"]

        columns[columns.index(old_name)] = new_name

    def __repr__(self):
        return "DataBase(name={})".format(self.name)
