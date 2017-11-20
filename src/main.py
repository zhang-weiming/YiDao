from qa import answer
import json

# 判断新问题
question = input('Input: ')
while question != 'EXIT':
    answers = answer(question)
    print('\nAnswer:')
    print(json.loads(answers))
    # if len(answers) > 0:
    #     a = 1
    #     for ans in answers:
    #         print( '\t[', a, '] ' + str(ans[0]) )
    #         print( '\t' + str(ans[1]).strip() )
    #         a += 1
    # else:
    #     print('\t抱歉，我不太懂您的意思 u.u')
    question = input('Input: ')