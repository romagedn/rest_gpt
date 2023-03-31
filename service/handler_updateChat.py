import base64
import json
import logging
import sys
import openai

import tornado.gen
import tornado.web

from utils.responseHelper import ResponseHelper
from utils.utilsFile import UtilsFile


class Handler_updateChat(tornado.web.RequestHandler):
    initialized = False


    @tornado.gen.coroutine
    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.finish('copy')

    @tornado.gen.coroutine
    def post(self):
        self.dispose()


    def dispose(self):
        try:
            body = self.request.body
            content = json.loads(body)
            asks = content['asks']
            answers = content['answers']
            new_chat = content['new_chat']
            role = content['role']

            answer, history_prompts, history_answers = self.chat(asks, answers, new_chat, role)

            response = ResponseHelper.generateResponse(True)
            response['answer'] = answer
            response['asks'] = asks
            response['answers'] = answers

            self.write(json.dumps(response))
            self.finish()

        except Exception as e:
            print('server internal error')
            logging.exception(e)

            self.set_header("Content-Type", "text/plain")
            response = ResponseHelper.generateResponse(False)
            self.write(json.dumps(response))
            self.finish()


    def loadConfig(self):
        if Handler_updateChat.initialized:
            return

        filename = './config.txt'

        content = UtilsFile.readFileContent(filename)
        content = json.loads(content)

        Handler_updateChat.api_key = content['api_key']
        Handler_updateChat.initialized = True


    def chat2gpt(self, prompt, assistants, max_tokens=1024, n=1, temperature=0.5, stop=None,
             model="gpt-3.5-turbo"):
        messages = []
        for assistant in assistants:
            messages.append({
                "role": 'assistant',
                "content": assistant,
            })
        messages.append({
            "role": 'user',
            "content": prompt,
        })
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temperature,
        )
        return completion.choices[0].message.content


    def get_assistant_limit(self):
        assistant_limit = '''
        回答不要超过 512 个字和标点
        '''
        return assistant_limit


    def get_assistant_role(self, role_define):
        relationship = role_define['relationship']
        family = role_define['family']
        character = role_define['character']

        assistant_role = '''
        你扮演我的{}，
        咱们家里面的状况是：{}
        你的性格是：{}
        '''.format(relationship, family, character)
        return assistant_role


    def chat(self, history_prompts, history_answers, cur_prompt, role_define):
        self.loadConfig()
        if not Handler_updateChat.initialized:
            return ''

        assistant_limit = self.get_assistant_limit()
        assistant_role = self.get_assistant_role(role_define)

        # consist history prompt
        prompt = ""
        _history_prompts = history_prompts[-2:]
        _history_answers = history_answers[-2:]
        for i in range(len(_history_prompts)):
            prompt += 'ask:\n' + _history_prompts[i] + '\n'
            prompt += 'answer:\n' + _history_answers[i] + '\n'
        prompt += cur_prompt

        answer = self.chat2gpt(prompt, [assistant_limit, assistant_role])
        history_prompts.append(cur_prompt)
        history_answers.append(answer)

        return answer, history_prompts, history_answers

