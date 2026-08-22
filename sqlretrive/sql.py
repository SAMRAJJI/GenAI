import sqlite3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()


table_info = """
create table student (name varchar(25), class varchar(25), 
section varchar(25), marks int
);
"""
cursor.execute(table_info)

cursor.execute(''' insert into student values('sam', 'AIDA', 'A', 90)''')
cursor.execute(''' insert into student values('ishu', 'bed', 'A', 95)''')
cursor.execute(''' insert into student values('janu', 'msc', 'A', 70)''')
cursor.execute(''' insert into student values('avi', 'be', 'B', 91)''')

print("the inserted records are")
data = cursor.execute('''select * from student''')

for row in data:
    print(row)
    
connection.commit()
connection.close()