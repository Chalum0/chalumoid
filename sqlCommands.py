innitDataBase = '''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL)
'''
NewUserInDB = '''INSERT INTO user (username, password_hash) VALUES (?, ?)'''