from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celerytimer.celerytimer import TimingTasks

obj = TimingTasks(host='127.0.0.1', port=3306, user='root', password='123456', database='testdb')


@obj.executed_task(task="push_task", task_name="直播推送", flag="2001", sql_unique=["channel_id"], repeatable=False)
@shared_task
def push_data(executed_data, a):
    """
    :param executed_data: 过滤掉了已经执行的任务和超出未来的一小时的时间的数据：
        {1602305203: [{"channel_id": 522, "account_id": 83022258}]}
    :return:
    """
    print("值一：", executed_data)
    print("自定义值：", a)
    print("测试成功")
