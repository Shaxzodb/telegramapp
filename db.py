from sqlite3 import connect

db=connect("sqlite3.db")
cursor=db.cursor()
user=cursor.execute('''SELECT * FROM users''')
for i in user.fetchall():
    print(i)