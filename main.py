

import sys
import tornado.web
import tornado.ioloop
import tornado.httpserver
import openai
import json

from service.handler_updateChat import Handler_updateChat
from utils.utilsFile import UtilsFile



if __name__ == "__main__":
    application = sys.argv[0]
    print('application = ', application)
    print('waiting requesting ...')
    print('')

    filename = './config.txt'
    content = UtilsFile.readFileContent(filename)
    content = json.loads(content)
    openai.api_key = content['api_key']

    models = openai.Model.list()
    print('all available models:')
    for model in models.data:
        print(model)
    print('')

    print('\nservice is starting\n')

    application = tornado.web.Application([
        (r"/upload", Handler_updateChat),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(13131)
    tornado.ioloop.IOLoop.instance().start()


