# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import sys
import logging.handlers
from .sso_check import *;
import redis
from django.views.decorators.csrf import csrf_exempt
from .forms import nameSpaceForm
from .config_default import *
from imp import reload
from rediscluster import StrictRedisCluster

reload(sys)
configs = configs
logging.basicConfig()
logger = logging.getLogger("django")

redis_nodes = [{'host': '172.28.38.28', 'port': 7000},
               {'host': '172.28.38.29', 'port': 7000},
               {'host': '1172.28.38.44', 'port': 7000}
               ]
try:
    redisconn = StrictRedisCluster(startup_nodes=redis_nodes, decode_responses=True)
except Exception as e:
    logger.error("Connect Error!" + e)
pool = redis.ConnectionPool(host=configs.get("redis2master").get("host"),
                            port=configs.get("redis2master").get("port"),
                            db=configs.get("redis2master").get("db"))
rs = redis.StrictRedis(connection_pool=pool)

slavepool = redis.ConnectionPool(host=configs.get("redis2slave").get("host"),
                                 port=configs.get("redis2slave").get("port"),
                                 db=configs.get("redis2slave").get("db"))
slavers = redis.StrictRedis(connection_pool=slavepool)


def login(request):
    SSO_URL = "http://sso.qm.qianbao-inc.com/sso"
    SSO_LOGIN_URL = "%s?back=%s" % (SSO_URL + "/login", 'http://%s/' % request.get_host())
    # 通过session检查用户是否登陆
    return HttpResponseRedirect(SSO_LOGIN_URL + "redistools/search-form/")


def logout(request):
    SSO_URL = "http://sso.qm.qianbao-inc.com/sso"
    SSO_LOGIN_URL = "%s?back=%s" % (SSO_URL + "/logout", 'http://%s/' % request.get_host())
    # 通过session检查用户是否登陆
    return HttpResponseRedirect(SSO_LOGIN_URL + + "/redistools/login/")


# 表单
@csrf_exempt
@sso_check
def search_form(request):
    username = getuser(request)['username']
    if not username:
        return render_to_response('login.html')
    else:
        return render_to_response('search_form.html', {"username": username})


# 接收请求数据
@csrf_exempt
@sso_check
def search(request):
    request.encoding = 'utf-8'
    username = getuser(request)['username']
    if not username:
        return render_to_response('login.html')
    else:
        if request.method == "POST":
            form = nameSpaceForm(request.POST)
            if form.is_valid():
                redistype = form.cleaned_data['redistype']
                namespace = form.cleaned_data['namespace']
                logger.info(
                    '用户为:"%s",查询类型为:"%s","namespace":"%s"}' % (username, redistype, namespace))
                if (int(redistype) == 3):

                    try:
                        result_list = redisconn.get(str(namespace))
                        # logger.info(type(result_list))
                        ll = []
                        ll.append(result_list)
                        logger.info(
                            u'查询成功=====用户为:"%s",查询详细信息为:"%s","namespace":"%s"' % (
                                username, redistype, namespace) + u"返回结果为：" + str(result_list))
                        # logger.info(list(result_list))
                        return render_to_response('result.html', {"result_list": ll, "keys": namespace})
                    except BaseException as e:
                        logger.error(e)
                        error = e
                    return render_to_response(('error.html', {"error": error}))
                else:

                    redis2keys = str(namespace)
                    try:
                        result_list = rs.get(redis2keys)
                        logger.info(result_list)
                        logger.info(type(result_list))
                        if result_list != None:
                            result_list = result_list.decode('utf-8')
                            ll = []
                            ll.append(result_list)
                        else:
                            ll = ["该key不存在"]
                        logger.info(
                            u'查询成功=====用户为:"%s",查询详细信息为:"%s","namespace":"%s"}' % (
                                username, redistype, namespace) + u"返回结果为：" + str(result_list))

                    except BaseException as e:
                        logger.error(e)
                        return render_to_response('error.html', {"error": e})
                    return render_to_response('result.html', {"result_list": ll, "keys": namespace})
            else:
                error = form.errors
                logger.error(error)
                return render_to_response('error.html', {"error": error})

        else:
            form = nameSpaceForm()


@csrf_exempt
@sso_check
def delete(request):
    request.encoding = 'utf-8'
    username = getuser(request)['username']
    if not username:
        return render_to_response('login.html')
    else:
        if request.method == "POST":
            form = nameSpaceForm(request.POST)
            if form.is_valid():
                redistype = form.cleaned_data['redistype']
                namespace = form.cleaned_data['namespace']
                logger.info(
                    '用户为:"%s",删除类型为:"%s","namespace":"%s"}' % (username, redistype, namespace))
                if (int(redistype) == 3):
                    result_list = redisconn.delete(str(namespace))
                    ll = []
                    ll.append(result_list)
                    logger.info(
                        '删除成功=====用户为:"%s",删除的详细信息为:"%s","namespace":"%s"' % (
                            username, redistype, namespace) + "返回结果为：" + str(result_list))

                    return render_to_response('result.html', {"result_list": ll, "keys": namespace})
                else:

                    redis2keys = str(namespace)
                    try:
                        result_list = rs.delete(redis2keys)
                        ll = []
                        ll.append(result_list)
                        logger.info(
                            '删除成功=====用户为:"%s",删除的详细信息为:"%s","namespace":"%s"' % (
                                username, redistype, namespace) + u"返回结果为：" + str(result_list))
                    except BaseException as e:
                        logger.error(e)
                    return render_to_response('result.html', {"result_list": ll, "keys": namespace})
            else:
                error = form.errors
                logger.error(error)
                return render_to_response('error.html', {"error": error})
        else:
            form = nameSpaceForm()


@csrf_exempt
@sso_check
def searchKeys(request):
    request.encoding = 'utf-8'
    username = getuser(request)['username']
    if not username:
        return render_to_response('login.html')
    else:
        if request.method == "POST":
            form = nameSpaceForm(request.POST)
            if form.is_valid():
                redistype = form.cleaned_data['redistype']
                namespace = form.cleaned_data['namespace']
                logger.info(
                    '用户为:"%s",查找类型为:"%s","namespace":"%s"}' % (username, redistype, namespace))
                if (int(redistype) == 3):
                    key = '*' + namespace + '*'
                    result_list = redisconn.scan(0, key)
                    ll = []
                    for l1 in result_list:
                        tu = result_list[l1]
                        ll = tu[1] + ll

                    logger.info(
                        '查找成功=====用户为:"%s",查找的详细信息为:类型:"%s","namespace":"%s"' % (
                            username, redistype, namespace) + "返回结果为：" + str(result_list))

                    return render_to_response('result.html', {"result_list": ll, "keys": namespace})
                else:

                    redis2keys = str("*" + namespace + "*")
                    try:
                        result_list = list(
                            map(lambda x: str(x).replace('b\'', '').replace('\'', ''), slavers.keys(redis2keys)))
                        # print(result_list)
                        logger.info(
                            '查找成功=====用户为:"%s",查找的详细信息为:"%s","namespace":"%s"' % (
                                username, redistype, namespace) + u"返回结果为：" + str(result_list))
                    except BaseException as e:
                        logger.error(e)
                    return render_to_response('result.html', {"result_list": result_list, "keys": namespace})
            else:
                error = form.errors
                logger.error(error)
                return render_to_response('error.html', {"error": error})
        else:
            form = nameSpaceForm()
