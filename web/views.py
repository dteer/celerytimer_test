from django.http import JsonResponse
from web.tasks import push_data


# Create your views here.


def index(request):
    # 把某个时间段的直播进行定时推送
    executed_data = {
        1602317898: [
            {"channel_id": "A", "coupon_price": [12, 23]},
            {"channel_id": "B", "coupon_price": [12, 23]},
        ],  # 会执行
        1602321498: [
            {"channel_id": "C", "coupon_price": [12, 23]},
        ],  # 会执行
        1602325158: [
            {"channel_id": "D", "coupon_price": [12, 23]},
        ],  # 过滤掉，不执行
    }  # 把当前的时间戳修改（只执行一个小时内的任务）
    push_data(executed_data, "a")
    return JsonResponse({'code': 0, "data": 1})
