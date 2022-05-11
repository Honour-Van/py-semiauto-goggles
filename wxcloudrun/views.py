import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg
from django.db.utils import timezone
from wxcloudrun.models import Counters
from wxcloudrun.models import Position

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})


def position(request, _):
    """
    获取当前位置数据

     `` request `` 请求对象
    """
    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_position()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_position(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_position():
    """
    获取当前位置
    """

    try:
        data = Position.objects.filter(date=timezone.now()).order_by('-id')

        # TODO 滤波算法还需优化
        possible_record_num = 0
        basela = data[0].latitude
        baselo = data[0].longitude
        for record in data:
            if record.latitude - basela > 2e-4 or record.longitude - baselo > 2e-4:
                break
            possible_record_num += 1
        data = data[:possible_record_num]
        longitude = data.aggregate(Avg('longitude'))
        latitude = data.aggregate(Avg('latitude'))

    except Position.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': {'longitude':longitude, 'latitude':latitude}},
                        json_dumps_params={'ensure_ascii': False})


def update_position(request):
    """
    添加位置记录

    `` request `` 请求对象
    """

    logger.info('update_position req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'longitude' not in body or 'latitude' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '位置参数不完整'},
                            json_dumps_params={'ensure_ascii': False})

    try:
        data = Position()
        data.longitude = body['longitude']
        data.latitude = body['latitude']
        data.save()
        return JsonResponse({'code': 0, "data": {'longitude':data.longitude, 'latitude':data.latitude}},
                    json_dumps_params={'ensure_ascii': False})
    except Exception('Django Error during db saving'):
        logger.warning('数据插入数据库时出错')
        return JsonResponse({'code': -1, 'errorMsg': '数据插入数据库时出错'},
                    json_dumps_params={'ensure_ascii': False})
