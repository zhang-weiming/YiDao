import codecs


if __name__ == '__main__':
    fr = codecs.open('../data/synonym/word2vec.txt', 'r', 'utf-8')
    content = fr.read()
    fr.close()
    wordVecList = content.split('\r\n')
    wordVecList.remove( wordVecList[-1] )
    wordVecDict
    for wordVec in wordVecList:
        parts = wordVec.split('|')
        vec = parts[]
