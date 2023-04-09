


import requests
import json
import base64



# （。）句号很重要，否则gpt的回答是接着你说的补充，而不是独立的回答
conversations = [
    '爸爸，我是小明。',
    '我挺好的，这次期中考试我的成绩不错。',
    '哥哥说下周去上海出差，下个月回来。',
    '我下个月放假就回家，我都想吃妈妈包的饺子了。',
]


history_prompts = []
history_answers = []


for c in range(len(conversations)):
    cur_prompt = conversations[c]
    print('user:\n', cur_prompt, '\n')

    data = json.dumps({
        'asks': history_prompts,
        'answers': history_answers,
        'new_chat': cur_prompt,
        'scenario': '''
        扮演我的爸爸，性格沉稳，关心家人。和妈妈住在一起，已经都退休了。我还在上学，住在学校。哥哥已经工作了，在外面租房子住。我好久没回家了，一直在学校忙学习.
        '''
    })

    header = {
        "Content-Type": "text/plain",
    }
    response = requests.post(url='http://localhost:13131/upload', data=data, headers=header)
    # print(response.content)

    content = json.loads(response.content)
    answer = content['answer']
    history_prompts = content['asks']
    history_answers = content['answers']

    print('answer:\n', answer, '\n')
