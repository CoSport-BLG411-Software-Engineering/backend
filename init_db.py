import sqlite3

def readSQL(filename: str) -> list:
    with open(filename, 'r') as f:
        content = f.readlines()
    return content


connection = sqlite3.connect('database.db')

with open('tables.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

createStatements = readSQL('createStatements.sql')
for statement in createStatements:
    print(statement)
    if len(statement) > 5:
        cur.execute(statement)
        

connection.commit()
connection.close()
