# -*- coding: utf-8 -*-

import time
import pycurl
import util
import tornado.web
import hashlib
import tornado.ioloop
import xml.etree.ElementTree as ET
from io import BytesIO
import replyer

rules = []

# 微信开发者验证
class AuthenticationHandler(tornado.web.RequestHandler):
    def check(self):
        token = "isysu"
        signature = self.get_argument("signature", None)
        timestamp = self.get_argument("timestamp", None)
        nonce = self.get_argument("nonce", None)
        echostr = self.get_argument("echostr", None)
        if signature and timestamp and nonce:
            param = [token, timestamp, nonce]
            param.sort()
            sha = hashlib.sha1(("%s%s%s" % tuple(param)).encode()).hexdigest()
            if sha == signature:
                if echostr:
                    return echostr
                else:
                    return True
        return False

    def get(self):
        self.write(str(self.check()))

    def post(self, *args, **kwargs):
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text
        content = data.find('Content').text
        msgid = data.find('MsgId').text
        out = ''
        for item in rules:
            if (item.match(content)):
                out = item.makeXML(fromusername, tousername)
                print(out)
                break
        self.write(out)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")


def make_app():
    return tornado.web.Application([
        (r"/", AuthenticationHandler),
        (r"/hello", MainHandler),
    ])

if __name__ == "__main__":
    helper = util.Helper('wxb9db0419592dbe7f',
                         '3a54d5663c95800880c927b124a31ead')
    # helper.get_auto_reply()
    rules = replyer.create_rulers('rule.json')
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()