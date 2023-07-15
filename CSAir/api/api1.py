# 查询票价接口1
# 可获取当天所有航班信息
from datetime import datetime
import requests
from constant import *

# 问题：这个接口需要TOKEN和acw_sc__v3，一个管理登录状态，一个管理滑动验证码，待后续解决获取


import requests

cookies = {
    'TOKEN': 'cea811522b74405fb32a16c0281b5176',
    'acw_sc__v3': '64b1506d1a0c86d9d28716895c47f08333ef9bad',
}

headers = {
    'authority': 'm.csair.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://m.csair.com',
    'referer': 'https://m.csair.com/booking_new/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
}

params = {
    'type': 'MOBILE',
    'APPTYPE': 'touch',
    'chanel': 'touch',
    'lang': 'zh',
    # 获取时间戳并转换为字符串
    '_': str(datetime.now().timestamp()).replace('.', '')[:13],
    # 从时间戳转换为datetime对象，再转换为字符串 #datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    'timeZone': 'GMT+08:00',
    'osversion': 'Mozilla-5.0_AppleWebKit-537.36_Chrome-114.0.0.0_Mobile_Safari-537.36',
}

json_data = {
    'isLogin': True,
    'ffpNo': '415935288525',
    'adultNum': 1,
    'childNum': 0,
    'infantNum': 0,
    'flightType': '',
    'date': '20230820',
    'cities': {
        'depCity': 'TYN',
        'arrCity': 'CAN',
    },
    'depCityFlag': True,
    'arrCityFlag': True,
    'pkgId': 'KqjMhEqz0000',
    'soOrderNo': 'SO2306260045430',
    'newGroupBuyId': 'CSAIRXST02',
    'queryType': 'NGB',
    'ticket': 'seasonTicket',
}

response = requests.post(
    'https://m.csair.com/CSMBP/bookProcess/avPrice/getAvPrice',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.text)