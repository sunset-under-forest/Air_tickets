# 查询票价接口2
# 只可获取一天的最低票价，好处是不需要cookie
from datetime import datetime, timedelta
import requests
from constant import *
from time import time
import queue
import threading

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


# json_data = {
#     'depCity': 'TYN',
#     'arrCity': 'CAN',
#     'depCityFlag': True,
#     'arrCityFlag': True,
#     'newGroupBuyId': 'CSAIRXST02',
#     'segType': 'S',
#     'isInter': 'N',
#     'startDate': '2023-08-20',
#     'endDate': '2023-08-20',
# }
#
# print(json_data)
#
# response = requests.post(
#     'https://m.csair.com/CSMBP/bookProcess/minPrice/getB2EPriceCalendar',
#     params=params,
#     headers=headers,
#     json=json_data,
#     proxies=PROXIES,
# )
#
# print(response.json())


def get_min_price_a_day(date, dep_city=DEPARTURE_CITY, arr_city=ARRIVAL_CITY):
    """
    查询某一天的最低票价
    :param dep_city: 出发城市代码
    :param arr_city: 到达城市代码
    :param date: 日期
    :return: 最低票价
    """
    json_data = {
        'depCity': dep_city,
        'arrCity': arr_city,
        'depCityFlag': True,
        'arrCityFlag': True,
        'newGroupBuyId': 'CSAIRXST02',
        'segType': 'S',
        'isInter': 'N',
        'startDate': date,
        'endDate': date,
    }

    response = requests.post(
        'https://m.csair.com/CSMBP/bookProcess/minPrice/getB2EPriceCalendar',
        params=params,
        headers=headers,
        json=json_data,
        proxies=PROXIES,
    )
    response.raise_for_status()  # 如果响应状态码不是200，主动抛出异常
    print(response.json())
    return response.json()['FROMOFLIGHTS'][0]['FLIGHT'][0]['MINPRICE']


def get_min_price_a_day_multi_thread(q, date, dep_city=DEPARTURE_CITY, arr_city=ARRIVAL_CITY):
    """
    查询某一天的最低票价
    :param q: 队列
    :param dep_city: 出发城市代码
    :param arr_city: 到达城市代码
    :param date: 日期
    :return: 最低票价
    """
    try:
        q.put((date, get_min_price_a_day(date, dep_city, arr_city)))
    except Exception as e:
        print(e)


def get_min_price(dep_city=DEPARTURE_CITY, arr_city=ARRIVAL_CITY, start_date=None, end_date=None):
    """
    查询某一段时间内的最低票价（非多线程）
    :param dep_city: 出发城市代码
    :param arr_city: 到达城市代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 最低票价
    """
    if start_date is None:
        # 如果没有指定开始日期，则默认为7天后
        start_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # 如果没有指定结束日期，则默认为开始日期后14天
    if end_date is None:
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=13)).strftime('%Y-%m-%d')

    # 得出查询日期区间长度
    date_range = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1

    min_prices = []
    for i in range(date_range):
        date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        min_prices.append((date, get_min_price_a_day(date, dep_city, arr_city)))

    return min_prices


def get_min_price_multi_thread(dep_city=DEPARTURE_CITY, arr_city=ARRIVAL_CITY, start_date=None, end_date=None):
    """
    查询某一段时间内的最低票价（多线程）
    :param dep_city: 出发城市代码
    :param arr_city: 到达城市代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 最低票价
    """
    if start_date is None:
        # 如果没有指定开始日期，则默认为7天后
        start_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # 如果没有指定结束日期，则默认为开始日期后14天
    if end_date is None:
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=13)).strftime('%Y-%m-%d')

    # 得出查询日期区间长度
    date_range = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1

    min_prices = []
    threads = []
    q = queue.Queue()
    for i in range(date_range):
        date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        t = threading.Thread(target=get_min_price_a_day_multi_thread, args=(q, date, dep_city, arr_city))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    while not q.empty():
        min_prices.append(q.get())

    min_prices.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
    return min_prices


if __name__ == '__main__':
    start_time = time()
    print(get_min_price_multi_thread(start_date='2023-08-20', end_date='2023-08-28'))
    print(time() - start_time)
