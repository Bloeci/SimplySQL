#! /usr/bin/python3.7.6

"""
    Example 2:
    Get all rows of a datatable and run through them.
"""

from simplysql import DataBase

with DataBase("tests/Test.db") as DB:
    # get the first datatable
    DBTable = DB.first_table()
    # >>> print(DBTable.header())
    # >>> ['name', 'age', 'gender']

    # get all rows
    rows = DBTable.rows()
    # >>> print(rows.all())
    # >>> [DataRow(index=0), DataRow(index=1), DataRow(index=2), DataRow(index=3),
    #      DataRow(index=4), DataRow(index=5), DataRow(index=6)]

    # property names depend on header of datatable
    for row in rows:
        print(row.name, row.age, row.gender)
