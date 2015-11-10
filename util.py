# -*- coding: utf-8 -*-

import json
import pycurl
from io import BytesIO
from pprint import pprint


# 用于获取普通access_token
class Helper(object):
    appid = ""
    appsecret = ""

    def __init__(self, appid, appsecret):
        """
        :param appid: 微信公众平台的AppID
        :param appsecret: 微信公众平台的App秘钥
        :return: 返回普通access_token
        """
        self.appid = appid
        self.appsecret = appsecret

    def get_access_token(self):
        """
        用于获取普通access_token，此token在调用其他API时会使用到
        :return: 返回获取到的access_token
        """
        grt_token_url = "https://api.weixin.qq.com/cgi-bin/token?" \
                        "grant_type=client_credential&appid=" \
                        + self.appid + "&secret=" + self.appsecret
        buffer = BytesIO()
        get_token = pycurl.Curl()
        get_token.setopt(get_token.URL, grt_token_url)
        get_token.setopt(get_token.WRITEDATA, buffer)
        get_token.perform()
        get_token.close()
        code = buffer.getvalue().decode()
        return json.loads(code)['access_token']

    def get_auto_reply(self):
        """
        将现有的规则输出到文件
        :return: none
        """
        get_reply_rule_url = "https://api.weixin.qq.com/cgi-bin/" \
                             "get_current_autoreply_info?" \
                             "access_token=" + self.get_access_token()
        buffer = BytesIO()
        get_reply_rule = pycurl.Curl()
        get_reply_rule.setopt(get_reply_rule.URL, get_reply_rule_url)
        get_reply_rule.setopt(get_reply_rule.WRITEDATA, buffer)
        get_reply_rule.perform()
        get_reply_rule.close()
        if buffer.getvalue():
            data = json.loads(buffer.getvalue().decode())
            with open('rule.json', 'w') as f:
                json.dump(data, f)
            pprint(data)
        else:
            print("None")
