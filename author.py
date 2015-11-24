# -*- coding: utf-8 -*-

import hashlib
import xml.etree.ElementTree as ET

import tornado.ioloop
import tornado.web

import replyer
import util

rules = []

menuData = """
{
    "button":[
        {
            "name":"i学习",
            "sub_button":[
                {
                    "name":"校内常用网站",
                    "type":"view",
                    "url":"http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=205420177&idx=1&sn=127a582cd5adef81f22fdb3560e61672&scene=18#wechat_redirect"
                },
                {
                    "name":"中大校报",
                    "type":"view",
                    "url":"http://xiaobao.sysu.edu.cn/"
                },
                {
                    "name":"图书馆",
                    "type":"view",
                    "url":"http://library.sysu.edu.cn/"
                },
                {
                    "name":"选课",
                    "type":"view",
                    "url":"http://uems.sysu.edu.cn/elect/"
                }
            ]
        },
        {
            "name":"i生活",
            "sub_button":[
                {
                   "type":"media_id",
                   "name":"校车时刻表",
                   "media_id":"u8uPp_Xv-4FyRVPyTYou7ixpEKbWZC7w-a9bSUDZd19L3L_gnbKRQlwCB3pGIr7V"
                },
                {
                   "type":"view",
                   "name":"校内公号推荐",
                   "url":"http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=205422765&idx=1&sn=c86343adb5e1230545137736594c0720&scene=18#wechat_redirect"
                },
                {
                   "type":"view",
                   "name":"校区地图",
                   "url":"http://www.sysu.edu.cn/2012/cn/zjzd/zjzd02/index.htm"
                },
                {
                   "type":"view",
                   "name":"常用电话",
                   "url":"http://home.sysu.edu.cn/tele/otele.asp"
                },
                {
                   "type":"media_id",
                   "name":"中大校历",
                   "media_id":"GI1Tl2pOccBGncHVrwFVwBWzFKhqzmW3J7IIOlYzKADitHqWXBz84VyHwSk3sGl4"
                }
            ]
        },
         {
            "name":"i互动",
            "sub_button":[
                {
                   "type":"view",
                   "name":"欢迎来稿",
                   "url":"http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=208325182&idx=2&sn=35492466165661ce4323dcddb4b8c9d7&scene=18#wechat_redirect"
                },
                {
                   "type":"text",
                   "name":"联系我们",
                   "value":"中大官微iSYSU期待您的踊跃投稿，为您的精彩提供展现平台。我们也欢迎您真诚的反馈与建议，我们立志于更好。来稿请投：zhongdaguanwei@163.com，您对iSYSU的意见和建议可直接回复至微信后台。感谢您对iSYSU的支持！mo-示爱"
                },
                {
                   "type":"view",
                   "name":"互动游戏",
                   "url":""
                },
            ]
        }
    ]
}
"""


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
        pass


def make_app():
    return tornado.web.Application([
        (r"/", AuthenticationHandler),
        (r"/hello", MainHandler),
    ])

if __name__ == "__main__":
    helper = util.Helper('wxb9db0419592dbe7f',
                         '3a54d5663c95800880c927b124a31ead')
    # helper.getAutoReply()
    rules = replyer.create_rulers('rule.json')
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
