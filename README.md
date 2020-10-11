基于celery实现的一个定时器

# 1. 项目启动

## 1.1  安装

* ```text
  pip install requestments.txt
  ```

## 1.2 工作前准备

* 启动django

  * ```
    python manage.py runserver 127.0.0.1:8000
    ```

* 启动celery

  * ```text
    celery -A celerytimer_test worker -l info -P eventlet
    celery -A celerytimer_test beat -l info
    ```

## 1.3 执行任务

* ```tex
  通过浏览器访问：http://127.0.0.1:8000/app
  ```

## 1.4 执行效果

* ```json
  1. 当执行任务后，会在数据库上生成一张新表 celery_timer
  2. 从表中可以看出任务的执行状况
  ```

# 2. celerytimer

## 2.1 功能介绍

### 1. 功能点

* 可动态配置`当前时间+-1小时`某个时间应该执行的任务，`已过期的任务也会执行`
* 过滤已经执行的任务

### 2.任务表 celery_timer

  * | 参数          | 类型                | 说明           | 备注                          |
    | ------------- | ------------------- | -------------- | ----------------------------- |
    | id            | int                 | 主键           |                               |
    | task          | str(255)            | 任务名         | 非中文                        |
    | task_name     | str(255)            | 任务昵称       |                               |
    | flag          | str(255)            | 任务标识       | 同一任务不同标识              |
    | key           | str(255) `唯一索引` | 唯一key        | 查找该任务的唯一key值         |
    | status        | int                 | 任务状态       | 0未执行，1执行成功，2执行失败 |
    | executed_time | datetime            | 任务应执行时间 |                               |
    | finish_time   | datetime            | 任务完成时间   |                               |
    | update_time   | datetime            | 更新时间       |                               |
    | create_time   | datetime            | 创建时间       |                               |

### 3.函数介绍

```python
def executed_task(self, task: str, task_name: str, flag: str, executed_data: dict, sql_unique: list,
                    repeatable: bool) -> dict:
    """数据检查校验
        Keyword Arguments:
            ----
            task: 任务名
            task_name: 任务昵称
            flag: 任务标识
            executed_data: 执行任务的数据 {时间戳:[{“account_id”:12,"channel_id":124},{},..],时间戳}
            sql_unique: 数据库唯一索引，从executed_data中获取该字段的值
            repeatable: 可以重复执行(默认False)，对应的是数据库
        """
```



## 2.2 使用说明

* 任务数据

  * ```json
    1602349200：2020-10-11 1:00:00
    1602349200：2020-10-11 2:00:00
    1602349200：2020-10-11 3:05:00
    现有一个任务：某时间(时间戳) 1602349200有专栏 ，B；某时间(时间戳) 1602352800有专栏C ，某时间(时间戳) 1602356700有专栏D
    需要到点告知就用户直播开始了
    当前时间为：2020-10-11 2:00:00
    
    executed_data = {
        1602349200:[
            {"channel_id":"A", "coupon_price":[12,23]},
            {"channel_id":"B", "coupon_price":[12,23]},
        ],	#会执行
        1602352800:[
            {"channel_id":"C", "coupon_price":[12,23]},
        ],	# 会执行
        1602356700:[
            {"channel_id":"D", "coupon_price":[12,23]},
        ],	# 过滤掉，不执行
    }
    ```

    

### 1. 任务定义

> 参考 ./celerytimer_test/web/tasks.py

* ```python
  from celery import shared_task
  from celerytimer.celerytimer import TimingTasks
  obj = TimingTasks(host='127.0.0.1', port=3306, user='root', password='123456', database='testdb')
  
  @obj.executed_task(task="The live broadcast begins", task_name="直播开始啦", flag="1", sql_unique=["channel_id"], repeatable=False)
  @shared_task
  def push_data(executed_data, *wargs,**kwargs):
      # executed_data 过滤后可以被执行的任务
      # 查找该专栏下所有的用户并告知
  ```

* 装饰器顺序

  >  obj.executed_task装饰器必须在shared_task前面

  

* 函数定义

  > push_data第一个参数必须是executed_data

  当executed_data经过任务器过滤，如果为空则不会执行push_data函数

* 参数定义

  * ```json
    sql_unique中对应的是executed_data中的某个元素
    
    即：
    executed_data = {
        1602349200:[
            {"channel_id":"A", "coupon_price":[12,23]},
            {"channel_id":"B", "coupon_price":[12,23]},
        ],
        1602352800:[
            {"channel_id":"C", "coupon_price":[12,23]},
        ],	
        1602356700:[
            {"channel_id":"D", "coupon_price":[12,23]},
        ],	
    }
    sql_unique中的元素必须在executed_data的指定位置中，且`只能为字符串或者数值`
    	
    ```

    

### 2. 任务执行

> 参考 ./celerytimer_test/web/views.py

* ```python
  push_data(executed_data, "a")
  ```



## 2.3 使用建议

​	建议使用该模块是以任务为单位

# 4.历史

## V1.1 （2020年10月09日）

- 基于celery的定时器

