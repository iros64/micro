import sqlite3

len_text = 0

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
question TEXT NOT NULL,
answer0 TEXT NOT NULL,
answer1 TEXT NOT NULL,
answer2 TEXT NOT NULL,
answer3 TEXT NOT NULL,
answertf0 TEXT,
answertf1 TEXT,
answertf2 TEXT,
answertf3 TEXT 
)
''')
cursor.execute("DELETE FROM users")
with open('a.txt', 'r', encoding='UTF-8') as file:
    lines = file.readlines()
    len_text = len(lines)
    for i in range(len_text):  
        lines[i] = lines[i].strip()
    for i in range(0, len_text, 10):
        cursor.execute(
        'INSERT INTO Users (question, answer0, answer1, answer2, answer3, answertf0, answertf1, answertf2, answertf3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            lines[i], lines[i+1], lines[i+2], lines[i+3], lines[i+4], lines[i+5], lines[i+6], lines[i+7], lines[i+8]
            )
        )
    connection.commit()
    connection.close()
def after_end():
    return len_text//10
def end(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    a = []
    xs = ["question", "answer0", "answer1", "answer2", "answer3", "answertf0", "answertf1", "answertf2", "answertf3"]
    for x in xs:
        cursor.execute(f"SELECT {x} FROM users WHERE id = {id}")
        row = cursor.fetchone()
        if row:
            a.append(row[0])
    connection.commit()
    connection.close()
    return a



print(*end(3))

