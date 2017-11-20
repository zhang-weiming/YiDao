import jieba

jieba.add_word('我')

a = '我爱你中国'

print(jieba.lcut(a, cut_all=False))
print(jieba.lcut(a, cut_all=True))