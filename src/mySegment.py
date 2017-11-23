import os
import sys
import codecs
import jieba
import numpy as np
import math
import pymysql
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'
WORD_BANK_FILE_PATH = '../data/WordBank.txt'
STOP_WORD_FILE_PATH = '../data/stop_word_UTF_8.txt'
user = 'root'
password = 'keyan123'
dbName = 'railwayquestion'
tableName = 'question'

stopWordList = []
wordBank = []


# def loadDocs(filePath, encoding='utf-8'):
#     f = codecs.open(filePath, 'r', encoding=encoding)
#     content = f.read()
#     f.close()
#     text_list = content.split(NEW_LINE)
#     text_list.remove( text_list[-1] )
#     # for i in range(0, len(text_list)):
#     #     text_list[i] = text_list[i].strip()
#     return text_list

def calLen(vec):
    vec = np.mat(vec)
    num = (float)(vec * vec.T)
    return math.sqrt(num)

def norm(vec):
    vec = np.mat(vec)
    return vec / calLen(vec)

def cosSim(v1, v2):
    v1 = np.mat(v1)
    v2 = np.mat(v2)
    num = (float)(v1 * v2.T)
    return num

def toSet(mlist):
    temp = set()
    for elem in mlist:
        temp.add(elem)
    return temp

# 加载数据
def loadDocs(encoding='utf-8'):
    db = pymysql.connect("localhost", user, password, dbName, charset='utf8') # 连接数据库
    cursor = db.cursor() # 建立游标
    sql = 'select id, question from ' + tableName
    cursor.execute(sql) # 执行查询
    textList = list()
    for row in cursor.fetchall():
        row = list(row)
        row[1] = jieba.lcut(row[1])
        textList.append( row )
    return textList

# 建立词库
def buildWordBank():
    textList = loadDocs()
    wordBank = set()
    for doc in textList: # 遍历每一个文档
        for word in doc[1]: # 遍历一个文档中的每一个词语
            wordBank.add(word) # 加入set中
    fw = codecs.open(WORD_BANK_FILE_PATH, 'w', encoding='utf-8')
    a = 1
    b = 1
    for word in wordBank:
        if word not in stopWordList:
            fw.write(word + NEW_LINE)
            print('writting ', a)
            a += 1
        else:
            print(b, word)
            b += 1
    fw.close()
    print('writting finished')

    # print('共有数据', len(textList), '条')
    # for doc in textList:
    #     print('\t', doc)

# 加载词库
def loadWordBank():
    fr = codecs.open(WORD_BANK_FILE_PATH, 'r', encoding='utf-8')
    content = fr.read()
    fr.close()
    wordBank = content.split(NEW_LINE)
    wordBank.remove( wordBank[-1] )
    return wordBank

# 文本表示，词袋模型
def myBow():
    textList = loadDocs()
    for i in range(0, len(textList)): # 遍历每一个文档
        doc = textList[i]
        j = 0
        while j < len(doc[2]):
            if doc[2][j] in wordBank:
                doc[2][j] = wordBank.index( doc[2][j] ) # 把每个词都替换成对应的id
                j += 1
            else:
                doc[2].remove( doc[2][j] ) # 词库中没有该词，抛弃
    for i in range(0, len(textList)): # 遍历每一个文档
        doc = textList[i]
        words = list(toSet(doc[2]))
        words.sort()
        tempVector = '' # 向量字符串
        vectorLen = 0 # 向量的模
        for word in words: # 遍历一个文档中的所有词语，计算向量所有参数的平方和
            vectorLen += math.pow(doc[2].count(word), 2)
        vectorLen = math.sqrt(vectorLen)
        for word in words: # 遍历一个文档中的所有词语，整理向量字符串
            tempVector += str(word) + ':' + str( doc[2].count(word) / vectorLen ) + ' '
        textList[i][1] = tempVector.strip() # 去掉字符串前后空格
        # print('vectorLen', vectorLen, '\nvector', textList[i])
    return textList

# # 保存到数据库
# def save(textList):
#     db = pymysql.connect("localhost", user, password, dbName, charset='utf8') # 连接数据库
#     cursor = db.cursor() # 建立游标
#     a = 1
#     for doc in textList: # 遍历每一个文档
#         sql = "update question set vector='" + doc[1] + "' where id=" + str(doc[0]) + ";"
#         state = cursor.execute(sql) # 执行更新操作
#         print('update', a, 'state', state)
#         a += 1
#     db.commit() # 提交操作
#     cursor.close()
#     db.close()
    
# 加载停用词
def loadTYC():
    fr = codecs.open(STOP_WORD_FILE_PATH, 'r', encoding='utf-8')
    content = fr.read()
    fr.close()
    stop_word_list = content.split(NEW_LINE)
    stop_word_list.remove( stop_word_list[-1] )
    for i in range(0, len(stop_word_list)):
        stop_word_list[i] = stop_word_list[i].strip()
    return stop_word_list

'''
# 去停用词
def quTYC(text_list, flag_list, stop_word_list):
    for i in range(0, len(text_list)):
        j = 0
        while j < len(text_list[i][-1]):
            # word = text_list[i][-1][j]
            if text_list[i][-1][j] in stop_word_list:
                text_list[i][-1].remove( text_list[i][-1][j] )
                flag_list[i].remove( flag_list[i][j] )
            else:
                j += 1
        print('quTYC', i)
    return text_list, flag_list
'''


# 入口
if __name__ == '__main__':
    wordBank = loadWordBank()
    # # 建立词库
    # stopWordList = loadTYC()
    # buildWordBank()

    # 文本表示，并保存到数据库
    textList = myBow()
    # save(textList)
    pass
