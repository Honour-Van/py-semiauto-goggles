import json
import logging
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters
from wxcloudrun.models import Position

logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

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
    if 'id' not in body:
        body['id'] = 1 # 如果没有给出id，说明是默认用于调试端口用的1号位

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=body['id'])
        except Counters.DoesNotExist:
            data = Counters()
        data.id = body['id']
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=body['id'])
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
    # latitude, longitude = 39.9086, 116.3974
    try:
        data, created = Position.objects.get_or_create(id=1)
        latitude = data.latitude
        longitude = data.longitude

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

    logger.debug('update_position req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'longitude' not in body or 'latitude' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '位置参数不完整'},
                            json_dumps_params={'ensure_ascii': False})

    try:
        Position.objects.update_or_create(id=1, defaults={'longitude':body['longitude'], 'latitude':body['latitude']})
        print('position updated as:', body['longitude'], body['latitude'])
        return JsonResponse({'code': 0, "data": {'longitude':body['longitude'], 'latitude':body['latitude']}},
                    json_dumps_params={'ensure_ascii': False})
    except Exception('Django Error during db saving'):
        logger.warning('数据插入数据库时出错')
        return JsonResponse({'code': -1, 'errorMsg': '数据插入数据库时出错'},
                    json_dumps_params={'ensure_ascii': False})


def buzz(request, _):
    """
    

     `` request `` 请求对象
    """
    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_buzz()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_buzz(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp

buzz_state = 0 # 全局变量，用于记录当前buzz状态，表示蜂鸣器是否应当鸣响

def get_buzz():
    # 获取buzz状态
    global buzz_state

    ret_val = JsonResponse({'code': 0, 'data': buzz_state},
                            json_dumps_params={'ensure_ascii': False})
    if buzz_state:
        buzz_state = 0
    return ret_val

def update_buzz(request):
    """
    @Description:
    小程序调用，触发
    ---------
    @Param:
    `request` 请求对象
    ---------
    @Return:
    `rsp` 响应对象
    ---------
    """
    logger.debug('update_buzz req: {}'.format(request.body))
    
    print('buzzing')

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})
    global buzz_state
    if body['action'] == 'on':
        buzz_state = 1
    elif body['action'] == 'off':
        buzz_state = 0
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                            json_dumps_params={'ensure_ascii': False})

    return JsonResponse({'code': 0, 'data': body['action']})


def feedback(request, _):
    """
    @Description:
    定位服务评价反馈接口
    ---------
    @Param:
    request 请求对象
    -------
    """
    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_feedback()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp

def get_feedback():
    """
    feedback的GET请求接口
    """
    try:
        data = Counters.objects.get(id=2)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})

