# # -*- coding: utf-8 -*-
#
# import requests
# try:
#     import cookielib
# except:
#     import http.cookiejar as cookielib
# import re
#
# session = requests.session()
# session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("cookie未能加载")
# agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
# headers = {
#     "HOST": "www.zhihu.com",
#     "Referer": "https://www.zhihu.com",
#     "User-Agent": agent
# }
#
#
# def get_xsrf():
#
#     response = session.get("https://www.zhihu.com", headers=headers)
#     # print(response.text)
#     # text = '<input type="hidden" name="_xsrf" value="5d18489f2d60d89dbfad4bb99c660f12"/>'
#     # text = '<input type="hidden" name="_xsrf" value="a68dffb14fe75572f06f6c6a733c7764"/>'
#     match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
#     if match_obj:
#        return print(match_obj.group(1))
#     else:
#         return ""
#
# def get_index():
#     response = session.get("https://www.zhihu.com", headers=headers)
#     with open("index.html", "wb") as f:
#         f.write(response.text.encode("utf-8"))
#     print("ok")
#
#
# def zhihu_login(account, password):
#     #知乎登陆
#     if re.match("^1\d{10}", account):
#         print("手机号码登陆")
#         post_url = "https://www.zhihu.com/login/phone_num"
#         post_data = {
#             "_xsrf": get_xsrf(),
#             "phone_num": account,
#             "password": password
#         }
#         respose_text = session.post(post_url, data=post_data, headers=headers)
#         session.cookies.save()
#
# zhihu_login("18021301129", "yinghua123")
# get_index()

# -*- coding: utf-8 -*-
__author__ = 'bobby'

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}

def is_login():
    #通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")

def zhihu_login(account, password):
    #知乎登录
    if re.match("^1\d{10}", account):
        print ("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }
    else:
        if "@" in account:
            #判断用户名是否为邮箱
            print("邮箱方式登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()

zhihu_login("18021301129", "yinghua123")
get_index()
is_login()

