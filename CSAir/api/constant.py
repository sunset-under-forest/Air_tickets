# 全局常数配置
import base64

# request代理
PROXIES = {
    "http": "http://localhost:7890",
    "https": "http://localhost:7890",
}

# 查询日期范围
START_DATE = '2023-08-21'
END_DATE = '2023-08-27'

# 查询城市
DEPARTURE_CITY = 'TYN'
ARRIVAL_CITY = 'CAN'

# 价格阈值（低于该价格则发送邮件）
PRICE_THRESHOLD = 800

# 邮件发送配置
MAIL_HOST = "smtp.163.com"  # 设置服务器
MAIL_PORT = 465  # 设置服务器端口
MAIL_USER = base64.b64decode(b'c3BvbmdlYm9iNDA0QDE2My5jb20=').decode()  # 用户名
MAIL_PASS = base64.b64decode(b'SkJaTkZZWVlKSkxMWllUVw==').decode()  # 口令

# 邮件接收配置
MAIL_RECEIVERS = [base64.b64decode(b'MjEzMjc3OTY2MkBxcS5jb20=').decode(),
                 base64.b64decode(b'MTU0ODg5MjA5N0BxcS5jb20=').decode(), ]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
