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
VECTOR_D = 20
rate = 0.1

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
wordBank = loadWordBank(WORD_BANK_FILE_PAYH) # 加载词库
# weight = [[0 for i in range(len(wordBank))] for ii in range(len(VECTOR_D))] # 初始化权重矩阵（每一个词对应一个向量，维度为VECTOR_D）
# print(len(weight), len(weight[0]))
# maxVal = 6 / math.sqrt(VECTOR_D)
weight = {}
for w in wordBank:
    vec = []
    for i in range(VECTOR_D):
        num = random.random()
        if random.random() > 0.5:
            num = -num
        vec.append(num)
    weight[w] = norm(vec)
    # print('\t', weight[w])
# print(weight['理解'])
# print(weight['可'])
# exit(0)

fr = codecs.open('../test/qna.txt', 'r', 'utf-8')
content = fr.read() # 读取已知问题文本
fr.close()
questions = content.split(NEW_LINE)
questions.remove( questions[-1] )
try:
    for time in range(1, 5):
    # while True:
        # time = 1
        a = 1
        for word in wordBank:
            tempWB = wordBank[:]
            tempWB.remove(word)
            vec1 = weight[word] # 当前词的向量
            b = 1
            for q in questions: # 遍历所有问题文本
                q = jieba.lcut(q)
                if word in q:
                    q.remove(word)
                for w in q: # 遍历当前问题文本的所有词
                    # 减小正确元组之间的距离
                    vec2 = weight[w]
                    diff = rate * (vec1 - vec2)
                    vec1 = vec1 - diff
                    vec2 = vec2 + diff
                    # print('vec1', vec1)
                    # print('vec2', vec2)
                    # print('diff', diff)
                    # input('回车继续...')
                    weight[word] = vec1
                    weight[w] = vec2
                    try:
                        tempWB.remove(w)
                    except BaseException:
                        pass
                print('time %d' % time, '%3d' % a, ',', '%3d' % b)
                b += 1
            for w in tempWB:
                # 增大错误元组之间的距离
                vec2 = weight[w]
                diff = rate * (vec1 - vec2)
                vec1 = vec1 + diff
                vec2 = vec2 - diff
                # print('vec1', vec1)
                # print('vec2', vec2)
                # print('diff', diff)
                # input('回车继续...')
                weight[word] = vec1
                weight[w] = vec2
            a += 1 # 当前词id加 1
        # time += 1 # 训练次数加 1
except InterruptedError:
    input('回车继续...')
else:
    # 保存模型
    fw = codecs.open('../data/word2vec.txt', 'w', 'utf-8')
    a = 1
    for w in weight.keys():
        vec = weight[w].tolist()[0]
        vecStr = ''
        for v in vec:
            vecStr += str(v) + ' '
        fw.write(w + '|' + vecStr.strip() + NEW_LINE)
        print('writting', a)
        a += 1
    fw.close()
