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
WORD_TO_VECTOR_FILE_PATH = '../../data/synonym/word2vec.txt'
STOP_WORD_FILE_PATH = '../../data/stop_word_UTF_8.txt'
DOCS_FILE_PATH = '../../data/synonym/input.txt'

stopWordList = []

VECTOR_D = 20
rate = 0.1
times = 200


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

# 加载语料
def loadDocs(encoding='utf-8'):
    fr = codecs.open(DOCS_FILE_PATH, 'r', encoding=encoding)
    content = fr.read()
    fr.close()
    docs = content.split(NEW_LINE)
    docs.remove( docs[-1] )
    wordDict = {}
    for doc in docs:
        parts = doc.split(' ')
        wordDict[parts[0]] = parts[1:]
    return wordDict

if __name__ == '__main__':
    stopWordList = loadTYC() # 加载停用词
    wordBank = loadWordBank(WORD_BANK_FILE_PAYH) # 加载词库
    wordDict = loadDocs()
    weight = {}
    for w in wordBank:
        vec = []
        for i in range(VECTOR_D):
            num = random.random()
            if random.random() > 0.5:
                num = -num
            vec.append(num)
        weight[w] = norm(vec)
    try:
        for time in range(1, times + 1):
        # while True:
            # time = 1
            # a = 1
            # for word in wordBank: # 遍历所有词
            #     wordBag = wordBank[:]
            #     wordBag.remove(word)
            #     vec1 = weight[word] # 当前词的向量
                # b = 1
            for key in wordDict.keys(): # 遍历所有词
                wordBag = wordBank[:]
                wordBag.remove(key)
                tempWordBag = wordDict[key]
                vec1 = weight[key]
                for w in tempWordBag: # 遍历当前词的所有相关词
                    # 减小正确元组之间的距离
                    vec2 = weight[w]
                    diff = rate * (vec1 - vec2)
                    vec1 = vec1 - diff
                    vec2 = vec2 + diff
                    weight[key] = norm(vec1)
                    weight[w] = norm(vec2)
                    if w in wordBag:
                        wordBag.remove(w)
                # print('time: %2d ,\tw: %3d' % (time, a))
                # b += 1
                for w in wordBag:
                    # 增大错误元组之间的距离
                    vec2 = weight[w]
                    diff = rate * (vec1 - vec2)
                    vec1 = vec1 + diff
                    vec2 = vec2 - diff
                    weight[key] = norm(vec1)
                    weight[w] = norm(vec2)
                # print('time: %3d / %3d ,\tw: %3d' % (time, times, a))
                # a += 1 # 当前词id加 1
            print('time: %3d / %3d' % (time, times))
            # time += 1 # 训练次数加 1
    except InterruptedError:
        pass
    else:
        # 保存模型
        fw = codecs.open(WORD_TO_VECTOR_FILE_PATH, 'w', 'utf-8')
        a = 1
        for w in weight.keys():
            vec = weight[w].tolist()[0]
            writtingStr = w + ' '
            for v in vec:
                writtingStr += str(v) + ' '
            fw.write(writtingStr.strip() + NEW_LINE)
            print('finish', a)
            a += 1
        fw.close()
