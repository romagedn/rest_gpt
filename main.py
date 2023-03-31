

import sys
import tornado.web
import tornado.ioloop
import tornado.httpserver
import openai

from service.handler_updateChat import Handler_updateChat



if __name__ == "__main__":
    application = sys.argv[0]
    print('application = ', application)
    print('waiting requesting ...')
    print('')

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


