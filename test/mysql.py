import codecs
import pymysql
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'

db = pymysql.connect("localhost", "root", "keyan123", "railwayquestion", charset='utf8')
cursor = db.cursor()

sql = "select question from question;"
cursor.execute(sql)
# db.commit()

# questions = cursor.fetchall()
# word = input('Input:')
# while word != 'EXIT':
#     for q in questions:
#         if word in q[0]:
#             print('Q:', q)
#     word = input('Input:')

fw = codecs.open('qna.txt', 'w', encoding='utf-8')
a = 1
for row in cursor.fetchall():
    fw.write( str(row[0]).strip() + NEW_LINE)
    print('writting', a)
    a += 1
fw.close()

cursor.close()
db.close()