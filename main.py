

import sys
import tornado.web
import tornado.ioloop
import tornado.httpserver

from service.handler_updateChat import Handler_updateChat



if __name__ == "__main__":
    application = sys.argv[0]
    print('application = ', application)
    print('waiting requesting ...')
    print('')


    print('\nservice is starting\n')

    application = tornado.web.Application([
        (r"/upload", Handler_updateChat),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(13130)
    tornado.ioloop.IOLoop.instance().start()


