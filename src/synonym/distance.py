import codecs
import numpy as np
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'
WORD_TO_VECTOR_FILE_PATH = '../../data/synonym/word2vec.txt'


# 求余弦距离
def cosSim(v1, v2):
    v1 = np.mat(v1)
    v2 = np.mat(v2)
    num = (float)(v1 * v2.T)
    return num
# 求欧式距离
# def euSim(v1, v2):
#     v1 = np.mat(v1)
#     v2 = np.mat(v2)
#     return np.sqrt(np.sum(np.square(v1 - v2)))

# 加载词向量
def loadVectors():
    fr = codecs.open(WORD_TO_VECTOR_FILE_PATH, 'r', 'utf-8')
    content = fr.read()
    fr.close()
    vectors = content.split(NEW_LINE)
    vectors.remove( vectors[-1] )
    vecDict = {}
    for vector in vectors:
        parts = vector.split('|')
        vec = parts[1].split(' ')
        for i in range(len(vec)):
            vec[i] = float(vec[i])
        vecDict[parts[0]] = vec
    return vecDict

# 入口
if __name__ =='__main__':
    vecDict = loadVectors()
    words = input('Input:')
    words = words.split(' ')
    while words[0] != 'EXIT':
        if words[0] in vecDict.keys() and words[1] in vecDict.keys():
            print(words[0].strip(), words[1].strip(), '\t', cosSim( vecDict[words[0].strip()], vecDict[words[1].strip()] ))
        words = input('Input:')
        words = words.split(' ')
