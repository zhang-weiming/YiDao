import pymysql
import os
import codecs

DATA_DIR_PATH = '../../data/mysql/'

host = 'localhost'
user = 'root'
password = 'keyan123'
database = 'test_db'
port = 3306
charset = 'utf8'

table_question = 'question'

def init_db_conn():
    conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port, charset=charset)
    cursor = conn.cursor()
    return conn, cursor

def close_db_conn(conn, cursor):
    cursor.close()
    conn.close()

def get_question(conn, cursor):
    sql = 'select %s from %s;' % ('question', table_question)
    cursor.execute(sql)
    fw = codecs.open(DATA_DIR_PATH + 'questions.txt', 'w', 'utf-8')
    for res in cursor.fetchall():
        fw.write('')


if __name__ == '__main__':
    conn, cursor = init_db_conn()
    # sql = 'select %s from %s;' % ('id, answer', table_question)
    # cursor.execute(sql)
    # for res in cursor.fetchall():
    #     # print(res[0], res[1].strip())
    #     sql = 'update question set answer = "%s" where id = %d;' % (res[1].strip(), res[0])
    #     # print(sql)
    #     cursor.execute(sql)
    # conn.commit()
    # print('OK')
    close_db_conn(conn, cursor)
