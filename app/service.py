import tornado.web
import os.path

from handler import Handler


class Application(tornado.web.Application):

    def __init__(self):

        handlers = [
            (r'/mainpage/', Handler),

        ]

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "./static"),
            template_path=os.path.join(os.path.dirname(__file__), "./templates"),
            debug=True,
            )

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()
    app.listen(5001)
    print("run at the 5001 port. please access following url: http://<server's ip address>:5001/mainpage/")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()