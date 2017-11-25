import codecs
import jieba
import random
import math
import numpy as np
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'
WORD_BANK_FILE_PAYH = '../../data/WordBank.txt'
DOCS_FILE_PATH = '../../data/qna.txt'
INPUT_FILE_PATH = '../../data/synonym/input.txt'
STOP_WORD_FILE_PATH = '../../data/stop_word_UTF_8.txt'

wordBank = []
stopWordList = []

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

# 加载问题文本
def loadDocs(encoding='utf-8'):
    fr = codecs.open(DOCS_FILE_PATH, 'r', encoding=encoding)
    content = fr.read()
    fr.close()
    questions = content.split(NEW_LINE)
    questions.remove( questions[-1] )
    for i in range(len(questions)):
        questions[i] = jieba.lcut(questions[i])
        j = 0
        while j < len(questions[i]):
            if questions[i][j] in stopWordList:
                questions[i].remove( questions[i][j] )
            else:
                j += 1
    return questions

if __name__ == '__main__':
    wordBank = loadWordBank(WORD_BANK_FILE_PAYH) # 加载词库
    stopWordList = loadTYC() # 加载停用词
    questions = loadDocs()
    wordDict = {}
    a = 1
    for word in wordBank:
        tempList = []
        for q in questions:
            if word in q:
                tempList.extend(q)
        while word in tempList:
            tempList.remove(word)
            wordDict[word] = tempList
        # tempSet = toSet(tempList)
        # tempSet.remove(word)
        # wordDict[word] = list(tempSet)
        print('processing', a)
        a += 1
        # if a > 5:
        #     break
    fw = codecs.open(INPUT_FILE_PATH, 'w', 'utf-8')
    for k in wordDict.keys():
        tempStr = k + ' '
        for word in wordDict[k]:
            tempStr += word + ' '
        fw.write(tempStr.strip() + NEW_LINE)
    fw.close()
    # fw = codecs.open(INPUT_FILE_PATH, 'w', 'utf-8')
    # a -= 1
    # b = 1
    # for key in wordDict.keys():
    #     # print('\t', k, '->', wordDict[k])
    #     wordBag = wordDict[key]
    #     for word in wordBag:    
    #         tempWordBag = wordDict[word]
    #         if key in tempWordBag:
    #             tempWordBag.remove(key)
    #         wordDict[word] = tempWordBag
    #         fw.write('%s %s' % (key, word) + NEW_LINE)
    #     print('finish', b, '/', a)
    #     b += 1
    # fw.close()

