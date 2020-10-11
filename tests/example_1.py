#! /usr/bin/python3.7.6

"""
    Example 1:
    Connect a database, create tables and get all base informations about them.
"""

from simplysql import DataBase

with DataBase("tests/Test.db") as DB:
    # >>> print(DB)
    # >>> DataBase(name=Test.db)

    # create tables if they doesn't exists
    header = ["name", "age", "gender"]
    datatypes = ["TEXT", "INTEGER", "TEXT"]

    DB.create_table("Persons", header, datatypes)

    # look at all attributes of the database
    # >>> print(DB.attributes())
    # >>> ___DataBase___
    #     Name:               Test.db
    #     Filetype:           db
    #     Path:               .\simplysql\tests\Test.db
    #     Has tables:         True
    #     Number of tables:   2
    #     Tables:             ['Persons', 'Persons_2']

    DBTable = DB.table(0)  # DB.first_table() / DB.last_table()
    # >>> print(DBTable)
    # >>> DataTable(name=Persons)

    DBTable.insert_rows([("Karl", 29, "male"),
                         ("Norbert", 29, "male"),
                         ("Sophie", 41, "female"),
                         ("Peter", 31, "male"),
                         ("Maria", 15, "female"),
                         ("Max", 12, "male"),
                         ("Mai", 94, "female")])

    # look at all attributes of datatable
    # >>> print(DBTable.attributes())
    # >>> ___DataTable___
    #     Name:               Persons
    #     Parent:             DataBase(name=Test.db)
    #     Index:              0
    #     Empty:              False
    #     Shape:              (7, 3)
    #     Columns:            ['name', 'age', 'sex']
    #     Column data types:  ['TEXT', 'INTEGER', 'TEXT']
    #     Number of columns:  3
    #     Number of rows:     7

    # print datatable as table
    # >>> print(DBTable.as_table())
    # >>>   name    age gender
    #     0 Karl    29  male
    #     1 Norbert 29  male
    #     2 Sophie  41  female
    #     3 Peter   31  male
    #     4 Maria   15  female
    #     5 Max     12  male
    #     6 Mai     94  female

    # print datatable as table
    # >>> print(DBTable.as_list())
    # >>> [['Karl', 29, 'male'], ['Norbert', 29, 'male'], ['Sophie', 41, 'female'], ['Peter', 31, 'male'], ['Maria', 15, 'female'], ['Max', 12, 'male'], ['Mai', 94, 'female']]

    # print datatable as table
    # >>> print(DBTable.as_dict())
    # >>> {'name': ['Karl', 'Norbert', 'Sophie', 'Peter', 'Maria', 'Max', 'Mai'], 'age': [29, 29, 41, 31, 15, 12, 94], 'sex': ['male', 'male', 'female', 'male', 'female', 'male', 'female']}

    # print datatable as table
    # >>> print(DBTable.as_tuple())
    # >>> (('Karl', 29, 'male'), ('Norbert', 29, 'male'), ('Sophie', 41, 'female'), ('Peter', 31, 'male'), ('Maria', 15, 'female'), ('Max', 12, 'male'), ('Mai', 94, 'female'))
