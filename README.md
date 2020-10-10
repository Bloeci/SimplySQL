# SimplySQL - The easiest way to edit SQL databases!

With SimplySQL you can edit SQL databases without having to have a great understanding of SQL queries. Creating, reading or editing a database is made possible by simple python commands without the need for many lines of code.

## Overview

The following features are included:
* Open or create databases
* Open or create tables
* Run through all rows or columns, create them or delete them

*At this stage only the following databases are supported: SQLite.*

## Installation

The installation is possible in two ways: either fork this github repo or use Pypi via pip.

```
$ pip install simplysql
```

## Usage

Because SimplySQL should work without queries, it is only necessary to import DataBase from SimplySQL
```python
from simplysql import DataBase
```
From this moment the fun can begin. The next step is the assignment of the database. Two methods can be used for this. The first method is a direct assignment (whereby this must be closed again at the end of processing):

```python
DB = DataBase("test/Test.db")
...
DB.close()
```
Or you can choose the with-assignment:
```python
with DataBase("test/Test.db") as DB:
...
```
Grab a table and iterate over all rows:
```python
DBtable = DB.table(0)

for row in DBTable.rows():
    print(row.as_dict())
    
    # first row would be like:: {'name': 'Karl', 'age': 29, 'gender': 'female'}
```
Each entry in a row can be reached by several ways where the assignment via a name depends on the name of the table columns: ```row.name```, ```row["name"]``` or ```row[0]```
