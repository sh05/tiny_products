FILENAME = "path/to/lahman2016.sqlite"

# import `pandas` and `sqlite3`
import pandas as pd
import sqlite3

# Connecting to SQLite Database
conn = sqlite3.connect(FILENAME)

# Querying Database for all seasons where a team played 150 or more games and is still active today.
query = "select name from sqlite_master where type = 'table';"

# Creating dataframe from query.
tables = conn.execute(query).fetchall()

# schema
query = "select sql from sqlite_master where type = 'table' and name = ?;"
# num of record
# query = "select count(*) from ?;"
for t in tables:
    r = conn.execute(query, t).fetchone()
    print("TABLE: ", t[0])
    print("SCHEMA: ", r[0])
    print()
