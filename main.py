# 1 import
import sqlite3

# 2 create connector
# create if not exist
conn = sqlite3.connect('29_01_2025.db')

# feature: allow access column by name
# row['order_price'] instead of row[3]
# black-box
conn.row_factory = sqlite3.Row

# 3 create cursor
cursor = conn.cursor()


def execute_modify_query(_cursor, _conn, query, parameters=None) -> None:
    '''
    # PEP8
    :param parameters: input parameters to the query
    :param _cursor: sqlite cursor
    :param _conn:  sqlite connection
    :param query: sql string query
    :return: None
    '''
    if parameters is not None:
        _cursor.execute(query, parameters)
    else:
        _cursor.execute(query)
    _conn.commit()  # write the data into the db file


# 4b
execute_modify_query(cursor, conn, '''DROP TABLE IF EXISTS users''')
execute_modify_query(cursor, conn, '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text UNIQUE NOT NULL,
    pwd text NOT NULL check(length(pwd) >= 4),
    login_times integer
)
''')

# 4b
execute_modify_query(cursor, conn, '''
    INSERT INTO users (username, pwd, login_times)
    values 
    ('itay', '1234', 100),
    ('danny', 'abcd', 999),
    ('sharon', '1111', 3033);
''')


def execute_read_query(cursor, query, parameters=None):
    if parameters is not None:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    rows_results = cursor.fetchall()
    return rows_results


# 4a
rows = execute_read_query(cursor, '''
select * from users;
''')

answer = []
total = 0
for row in rows:
    # we did -- conn.row_factory = sqlite3.Row
    # recommended when we do not
    # want to make a list of ALL rows
    # or a dict PER row
    # and not access column by number
    print(row['username'])
    total += int(row['login_times'])

    # convert each row to --> list,tuple,dict
    # answer.append(list(row))
    # answer.append(tuple(row))
    answer.append(dict(row))

print('total is', total)
print(answer)
# ------------------------------------------------------------
while True:
    username = input("enter username")
    if username == 'exit':
        break
    pwd = input("enter password")
    get_user_query = 'select * from users where username=? and pwd=?'
    result = execute_read_query(cursor, get_user_query, (username, pwd))
    if len(result) > 0:
        print("user is exist already")
    else:
        insert_new_user_query = '''
        INSERT INTO users (username, pwd, login_times)
        values (?,?,0) '''
        execute_modify_query(cursor, conn, insert_new_user_query, (username, pwd))

# --------------------------------------------------------------------
while True:
    username = input("enter username")
    if username == 'exit':
        break
    pwd = input("enter password")
    get_user_query = 'select * from users where username=? and pwd=?'
    result = execute_read_query(cursor, get_user_query, (username, pwd))

    if len(list(result)) != 1:
        get_pwd_by_exist_user_query = 'select u.pwd from users u where username=?'
        result_user = execute_read_query(cursor, get_pwd_by_exist_user_query, (username,))
        if len(result_user) != 1:
            print("user doesn't exist")
        else:
            if result_user[0]['pwd'] != pwd:
                print("wrong pwd")
    else:
        print("login was successful")

        new_login_times = int(result[0]['login_times']) + 1
        update_login_amount = 'update users set login_times=? where username=?'
        execute_modify_query(cursor, conn, update_login_amount, (new_login_times, username))
    rows = execute_read_query(cursor, '''
                select * from users;
                ''')
    answer = [dict(r) for r in rows]
    print(answer)

# 5 close connection
conn.close()
# 1. add function for execute_read_query
# 2. write in a loop, until 'exit', or once:
#      input username
#      input password
#      insert these values into the table
#          login_times = 0
# 3. write in a loop, until 'exit', or once:
#      input username
#      input password
#      check if the user-password correct
#         print "login was successful"
#       bonus:
#       if not, check if the user exist-
#         if so print "wrong pwd"
#         if not print "user does not exist"
#      after successful login (update query):
#         add 1 into the user login_amount
