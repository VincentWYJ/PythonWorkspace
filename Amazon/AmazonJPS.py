# -*- coding: utf-8 -*-

import os
import http.cookiejar
from lxml import etree
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error


# 1、网站登录操作
login_url = 'https://www.amazon.co.jp/ap/signin?_encoding=UTF8&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2F%3Fref_%3Dnav_ya_signin'
values = {'email': '44059346@qq.com', 'password': '1qaz2wsx@19', 'submit': 'Login'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
request = urllib.request.Request(login_url, postdata, headers)

try:
    response = opener.open(request)
    page = response.read().decode()
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)
    
cookie.save(ignore_discard = True, ignore_expires = True)

print("Cookie info: ")
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)


# 2、数据获取操作
get_url = "https://www.amazon.co.jp/%E5%85%AB%E6%B5%B7%E5%B1%B1-%E5%85%AB%E6%B5%B7%E5%B1%B1-%E7%B4%94%E7%B1%B3%E5%90%9F%E9%86%B8-%EF%BC%88%E6%96%B0%E6%BD%9F%EF%BC%89-1-8L-1%E6%9C%AC/dp/B002LA0NUO/ref=sr_1_1?s=food-beverage&ie=UTF8&qid=1480987112&sr=1-1"
get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)

bsobj = BeautifulSoup(get_response.read().decode(), "html.parser")

print("\nProduct info: ")
for el in bsobj.find_all("span", {"id": "productTitle"}):
    print(el.get_text())

# id="brand" 产品品牌
for el in bsobj.find_all("a",{"id":"brand"}):
    print(el.get_text())
# id="acrCustomerReviewText" 评论数量
for el in bsobj.find_all("span",{"id":"acrCustomerReviewText"}):
    print(el.get_text())
# id="id="priceblock_ourprice"" 售价    
for el in bsobj.find_all("span",{"id":{"priceblock_ourprice","priceb"}}):
    print(el.get_text())

#id="price-shipping-message" 配送费
for el in bsobj.find_all("span",{"id":{"price-shipping-message"}}):
    print(el.get_text())

    # id="wayfinding-breadcrumbs_feature_div" 进入路径
for el in bsobj.find_all("a",{"class":"a-link-normal a-color-tertiary"}):
    print(el.get_text())
# id="productTitle" 产品标题


# id="price-shipping-message" 送货运费
for el in bsobj.find_all("span",{"id":"price-shipping-message"}):
    print(el.get_text())
    
# class="a-size-medium a-color-success" span 剩余多少

for el in bsobj.find_all("span",{"class":"a-size-medium a-color-success"}):
    print(el.get_text())

# id="ddmDeliveryMessage" div 是否直接送达该邮政号码
for el in bsobj.find_all("div",{"id":"ddmDeliveryMessage"}):
    print(el.get_text())

# id="merchant-info" div 快递单位
for el in bsobj.find_all("div",{"id":"merchant-info"}):
    print(el.get_text())