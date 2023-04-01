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
            scenario = content['scenario']

            answer, history_prompts, history_answers = self.chat(asks, answers, new_chat, scenario)

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


    def chat2gpt(self, prompt, assistants, max_tokens=1024, n=1, temperature=0.8, stop=None,
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
        回答不要超过 512 个字和标点，
        回复要自然，像真正的聊天一样
        '''
        return assistant_limit


    def chat(self, history_prompts, history_answers, cur_prompt, scenario):

        assistant_limit = self.get_assistant_limit()
        assistant_role = scenario['role']
        assistant_background = scenario['background']
        assistant_character = scenario['character']

        # consist history prompt
        prompt = ""
        _history_prompts = history_prompts[-2:]
        _history_answers = history_answers[-2:]
        for i in range(len(_history_prompts)):
            prompt += _history_prompts[i] + '\n'
            prompt += _history_answers[i] + '\n'
        prompt += cur_prompt

        answer = self.chat2gpt(prompt, [assistant_limit, assistant_role, assistant_background, assistant_character])
        history_prompts.append(cur_prompt)
        history_answers.append(answer)

        return answer, history_prompts, history_answers

