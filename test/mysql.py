import codecs
import pymysql
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'

db = pymysql.connect("localhost", "root", "keyan123", "railwayquestion", charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# 使用 execute()  方法执行 SQL 查询 
# cursor.execute("update question set vector=%s where id=%d;" % ('111', 1))
sql = "select question, answer from question;"
cursor.execute(sql)
# db.commit()
fw = codecs.open('qna.txt', 'w', encoding='utf-8')
a = 1
for row in cursor.fetchall():
    fw.write( str(row[0]).strip() + '|' + str(row[1]).strip() + NEW_LINE)
    print('writting', a)
    a += 1
fw.close()
# 关闭
cursor.close()
db.close()