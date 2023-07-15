from api2 import get_min_price_multi_thread
import smtplib
from email.mime.text import MIMEText
from constant import *


def send_mail(mail_receiver):
    print("开始发送邮件至" + mail_receiver + "...")
    msg = MIMEText('您关注的航班价格最低为' + str(min_price) + '元，以下是具体信息：\n' + note, 'plain', 'utf-8')
    msg['Subject'] = 'CSAir航班价格提醒'
    msg['From'] = MAIL_USER
    msg['To'] = mail_receiver

    smtp = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
    smtp.login(MAIL_USER, MAIL_PASS)
    smtp.sendmail(MAIL_USER, mail_receiver, msg.as_string())
    print("邮件发送成功！")
    smtp.quit()


if __name__ == '__main__':
    fight_info = get_min_price_multi_thread(start_date=START_DATE, end_date=END_DATE)
    note = ""
    min_price = 0xfffffff
    for fight in fight_info:
        min_price = min(min_price, int(fight[1]))
        if int(fight[1]) < PRICE_THRESHOLD:
            note += fight[0] + "\t\t" + fight[1] + "￥\n"

    if min_price < PRICE_THRESHOLD:
        for mail_receiver in MAIL_RECEIVERS:
            send_mail(mail_receiver)
