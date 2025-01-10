import sqlite3 as sq


async def db_connect() -> None:
    global db, cur
    db = sq.connect("Users.db")
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY UNIQUE ON CONFLICT IGNORE,\
         name TEXT)'
    )
    db.commit()


async def get_user(id) -> list:
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    user = cur.fetchone()
    print(cur.fetchall())
    db.commit()
    return user


async def get_users():
    users = cur.execute("SELECT * FROM users").fetchall()
    return users


async def del_user(id):
    sql_update_query = """DELETE from users where id = ?"""
    cur.execute(sql_update_query, (id,))


async def check_id(id):
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    row = cur.fetchone()
    print(row, " chek_id если нон то фолз")
    if row is None:
        return False
    db.commit()
    return True


async def add_id(id):
    cur.execute('SELECT COUNT(*) FROM users WHERE id = ?', (id,))
    result = cur.fetchone()[0]

    if result == 0:
        # Если записи с заданным id нет, то добавляем ее
        cur.execute('INSERT INTO users (id ) VALUES (?)', (id,))
        db.commit()
    db.commit()


async def update(user_id, first_name):
    name = first_name
    await add_id(user_id)
    cur.execute("UPDATE users SET name=? WHERE id=?",
                (name, user_id))
    db.commit()
