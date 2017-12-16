import jieba
import codecs
import platform

NEW_LINE = '\n'
if platform.system() == 'Windows':
    NEW_LINE = '\r\n'


# jieba.add_word('我')

# a = '我爱你中国'

# print(jieba.lcut(a, cut_all=False))
# print(jieba.lcut(a, cut_all=True))

fr = codecs.open('qna.txt', 'r', 'utf-8')
content = fr.read()
fr.close()

questions =content.split(NEW_LINE)
questions.remove( questions[-1] )

qInput = input('Input:')
while qInput != 'EXIT':
    qInput = jieba.lcut(qInput)
    num = []
    for q in questions:
        n = 0
        for w in qInput:
            if w in q:
                n += 1
        num.append(n)
    maxIndex = num.index( max(num) )
    num[maxIndex] = 0
    print('Q1:', questions[ maxIndex ])
    maxIndex = num.index( max(num) )
    num[maxIndex] = 0
    print('Q2:', questions[ maxIndex ])
    maxIndex = num.index( max(num) )
    print('Q3:', questions[ maxIndex ])
    qInput = input('Input:')
