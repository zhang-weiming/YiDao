import codecs
import jieba
import random
import math
import numpy as np
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'
WORD_BANK_FILE_PAYH = '../data/WordBank.txt'
DOCS_FILE_PATH = '../test/qna.txt'


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

# 加载问题文本
def loadDocs(encoding='utf-8'):
    fr = codecs.open(DOCS_FILE_PATH, 'r', encoding=encoding)
    content = fr.read()
    fr.close()
    questions = content.split(NEW_LINE)
    questions.remove( questions[-1] )
    for i in range(len(questions)):
        questions[i] = jieba.lcut(questions[i])
    return questions

if __name__ == '__main__':
    wordBank = loadWordBank(WORD_BANK_FILE_PAYH) # 加载词库
    questions = loadDocs()
    wordDict = {}
    a = 1
    for word in wordBank:
        tempList = []
        mWordBag = wordBank[:]
        mWordBag.remove(word)
        for q in questions:
            if word in q:
                tempList.extend(q)
        tempSet = toSet(tempList)
        wordDict[word] = list(tempSet)
        print('processing', a)
        a += 1
        if a > 5:
            break
    for k in wordDict.keys():
        print(k, '->', wordDict[k])

