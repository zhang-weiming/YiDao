import os
import sys
import codecs
import jieba
import numpy as np
import math
import pymysql
import platform
import time
import json
import random

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'
WORD_BANK_FILE_PAYH = '../data/WordBank.txt'
VECTORS_FILE_PAYH = '../data/vectors.txt'
STOP_WORD_FILE_PATH = '../data/stop_word_UTF_8.txt'

user = 'root'
password = 'keyan123'
dbName = 'railwayquestion'
tableName = 'question'

wordBank = []
vectors = []
stopWordList = []

# 求一个向量的模长
def calLen(vec):
    vec = np.mat(vec)
    num = (float)(vec * vec.T)
    return math.sqrt(num)
# 对向量单位化
def norm(vec):
    vec = np.mat(vec)
    vecLen = calLen(vec)
    if vecLen > 0:
        vec = vec / vecLen
    return vec
# 求余弦距离
def cosSim(v1, v2):
    v1 = np.mat(v1)
    v2 = np.mat(v2)
    num = (float)(v1 * v2.T)
    return num
# list转set
def toSet(mlist):
    temp = set()
    for elem in mlist:
        temp.add(elem)
    return temp

# 加载词库
def loadWordBank(filePath):
    fr = codecs.open(filePath, 'r', encoding='utf-8')
    content = fr.read()
    fr.close()
    wordBank = content.split(NEW_LINE)
    wordBank.remove( wordBank[-1] )
    return wordBank

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

# 给问题question匹配合适的答案
def answer(question):
    t1 = time.time()
    # 分词
    question = jieba.lcut(question) # 分词
    i = 0
    # 把每个词都替换成对应的id，词库中没有则抛弃
    while i < len(question):
        if question[i] in stopWordList:
            question.remove( question[i] )
        else:
            if question[i] in wordBank:
                # 把每个词都替换成对应的id
                question[i] = wordBank.index( question[i] )
                i += 1
            else:
                # 词库中没有该词，替换可能的近义词
                synonym = procSynonym(question[i])
                print('\t[procSynonym]',question[i], '->',  synonym)
                if len(synonym) > 0:
                    question[i] = wordBank.index( synonym[random.randint(0, len(synonym) - 1)] )
                    i += 1
                else:
                    question.remove( question[i] )
    # 将问题文本表示为向量
    words = list(toSet(question))
    words.sort()
    vector = [0 for ii in range(0, len(wordBank))]
    for word in words:
        vector[word] = question.count(word)
    # if calLen(vector) > 0:
    vector = norm(vector) # 问题文本的向量
    # 计算 该问题向量 和 所有已知问题向量 的余弦相似度
    sims = []
    for doc in vectors:
        vec = doc[1]
        sim = cosSim(vector, vec) # 计算余弦距离
        sims.append(sim)
        # if sim > maxSim:
        #     maxSim = sim # 更新最近问题的余弦距离
        #     indexOfSim = doc[0] # 最近问题的id（此处变量类型为字符串，便于组织sql语句）
    indexs = []
    ansCnt = len(sims) - sims.count(0)
    # 非零的相似度距离分数 按 三个以上 和 以下 分类处理
    if ansCnt > 2:
        ansCnt = 3
    for i in range(0, ansCnt):
        maxIdx = sims.index( max(sims) ) # 当前最大值的索引
        sims[maxIdx] = 0 # 当前最大值归零，相当于删除该值
        indexs.append(maxIdx + 1) # 记录当前最大值的索引值 + 1，加1 是因为数据库中的id比这里的索引值大1
    print('MaxSimIndexs', indexs)
    if len(indexs) > 0:
        answers = getAnswersFromDB(indexs)
        for i in range(0, len(answers)):
            ans = answers[i]
            ansJson = dict() # 近义问题与答案的dict，方便后面转换为json格式
            ansJson['question'] = str(ans[0]).strip()
            ansJson['answer'] = str(ans[1]).strip()
            answers[i] = ansJson
        return json.dumps(answers, ensure_ascii=False) # 以json格式返回结果
    else:
        # 没有找到答案，返回空
        return str(json.dumps([]))

# 从数据库中获取 特定id 的问题-答案集
def getAnswersFromDB(indexs):
    # t1 = time.time()
    db = pymysql.connect("localhost", user, password, dbName, charset='utf8') # 连接数据库
    cursor = db.cursor() # 建立游标
    answers = []
    sql = "select question, answer from question where id=%d;"
    for index in indexs:
        cursor.execute(sql % index) # 执行查询
        ans = cursor.fetchone()
        answers.append(ans)
    # 关闭数据库连接
    cursor.close()
    db.close()
    # print('\t[getAnswers]', time.time() - t1)
    return answers

# 读取向量
# 参数 wordBankLen ，是词库的长度
def loadVectors(wordBankLen):
    try:
        fr = codecs.open(VECTORS_FILE_PAYH, 'r', encoding='utf-8')
        content = fr.read() # 读文件
    except IOError:
        print('[Error] 读取词库文件失败')
        return []
    else:
        fr.close() # 关闭文件
    vectors = content.split(NEW_LINE) # 按行分割
    vectors.remove( vectors[-1] ) # 去掉末尾的空元素
    for i in range(0, len(vectors)):
        vectorInfo = vectors[i]
        vectorInfo = vectorInfo.split('|') # [id, 'index:value ...'] 具体结构参考 ../data/vectors.txt
        tempVector = [0 for i in range(0, wordBankLen)]
        parts = vectorInfo[1].split(' ')
        for part in parts:
            indexAndNum = part.split(':')
            tempVector[int(indexAndNum[0])] = float(indexAndNum[1]) # 整理向量各维度参数
        vectorInfo[1] = tempVector
        vectors[i] = vectorInfo # （覆盖）保存为 vectors 中的第 i 个元素
    return vectors
'''
# 读取向量
def loadVector(wordBankLen):
    db = pymysql.connect("localhost", user, password, dbName, charset='utf8') # 连接数据库
    cursor = db.cursor() # 建立游标
    sql = "select id, vector from question;"
    cursor.execute(sql) # 执行查询
    vectors = []
    for row in cursor.fetchall():
        vectorInfo = list()
        vectorInfo.append(str(row[0])) # id
        tempVector = [0 for i in range(0, wordBankLen)]
        parts = row[1].split(' ')
        for part in parts:
            indexAndNum = part.split(':')
            tempVector[int(indexAndNum[0])] = float(indexAndNum[1]) # 整理向量各维度参数
        vectorInfo.append(tempVector)
        vectors.append(vectorInfo)
    cursor.close()
    db.close()
    return vectors
'''

# 可能近义词处理
def procSynonym(word):
    word = list(word)
    words = []
    flag = False
    for w in word:
        for ww in wordBank:
            if w in ww:
                words.append(ww)
                flag = True
                break
        if flag:
            break
    return words
def loadWordVec():
    pass


wordBank = loadWordBank(WORD_BANK_FILE_PAYH) # 加载词库
vectors = loadVectors(len(wordBank)) # 加载已知问题的向量
stopWordList = loadTYC() # 加载停用词
jieba.lcut('test')

# 入口
if __name__ == '__main__':
    # 判断新问题
    question = input('Input: ')
    while question != 'EXIT':
        answers = answer(question)
        print('\nAnswer:')
        for ans in answers:
            print(ans)
        question = input('Input: ')
