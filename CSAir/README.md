## 项目介绍

### 本项目是针对中国南方航空（CSAir）的学生飞机票活动的机票价格监控

- 活动地址（基于项目创建）：[https://m.csair.com/FTPCMS/cn/touchad/2021/20210325/index.html](https://m.csair.com/FTPCMS/cn/touchad/2021/20210325/index.html)
- 活动规则（本地保存）：[./resource/html/“学生旅行”2023版产品规则.html](./resource/html/“学生旅行”2023版产品规则.html)
- 目前已支持出发地，目的地，出发日期区间以及邮件通知功能


## 使用方法
```
配置constans.py中的参数
通过`python app.py`运行程序即可
还可设置定时任务，定时运行程序以实现定时监控
```