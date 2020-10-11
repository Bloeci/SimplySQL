#! /usr/bin/python3.7.6

"""
    Example 2:
    Get all columns of a datatable and run through them.
"""

from simplysql import DataBase

with DataBase("tests/Test.db") as DB:
    # get the first datatable
    DBTable = DB.first_table()
    # >>> print(DBTable.header())
    # >>> ['name', 'age', 'gender']

    # get all columns
    columns = DBTable.columns()
    # >>> print(columns.all())
    # >>> DataColumn(index=0), DataColumn(index=1), DataColumn(index=2)]

    for column in columns:
        print(column.header(), column[0])
