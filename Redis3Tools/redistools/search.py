# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import sys
import logging.handlers
from sso_check import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import nameSpaceForm
import config_default, redis

reload(sys)
sys.setdefaultencoding("utf-8")
configs = config_default.configs
logging.basicConfig()
logger = logging.getLogger("django")


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
                keys = form.cleaned_data['keys']
                logger.info(
                    '用户为:"%s",查询类型为:"%s","namespace":"%s", "key":"%s"}' % (username, redistype, namespace, keys))
                if (int(redistype) == 3):
                    uri_get = 'redis/v1/get'
                    get_k = '{"namespace":"%s", "key":"%s"}' % (namespace, keys)
                    try:
                        res = requests.post(url=configs.get("redis3").get("url") + uri_get, data=get_k,
                                            headers={'Content-Type': 'application/json;charset=utf-8'})
                        result_list = json.JSONDecoder().decode(res.text)["result"]
                        logger.info(
                            '查询成功=====用户为:"%s",查询详细信息为:"%s","namespace":"%s", "key":"%s"' % (
                                username, redistype, namespace, keys) + "返回结果为：" + result_list)
                        return render_to_response('result.html', {"result_list": result_list, "keys": keys})
                    except BaseException, e:
                        logger.error(e)
                        error = e
                    return render_to_response(('error.html', {"error": error}))
                else:
                    pool = redis.ConnectionPool(host=configs.get("redis2").get("host"),
                                                port=configs.get("redis2").get("port"),
                                                db=configs.get("redis2").get("db"))
                    rs = redis.StrictRedis(connection_pool=pool)
                    redis2keys = str(namespace+keys)
                    try:
                        result_list = str(rs.get(redis2keys))
                        logger.info(
                            '查询成功=====用户为:"%s",查询详细信息为:"%s","namespace":"%s", "key":"%s"}' % (
                                username, redistype, namespace, keys) + "返回结果为：" + result_list)

                    except BaseException, e:
                        logger.error(e)
                        return render_to_response('error.html', {"error": e})
                    return render_to_response('result.html', {"result_list": result_list, "keys": keys})
            else:
                error = form.errors
                logger.error(error)
                return render_to_response('error.html', {"error": error})

        else:
            form = nameSpaceForm()


@sso_check
@csrf_exempt
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
                namespace = form.cleaned_data['nameSpace']
                keys = form.cleaned_data['keys']
                logger.info(
                    '用户为:"%s",删除类型为:"%s","namespace":"%s", "key":"%s"}' % (username, redistype, namespace, keys))
                if (int(redistype) == 3):
                    uri_get = 'redis/v1/del'
                    get_k = '{"namespace":"%s", "key":"%s"}' % (namespace, keys)
                    res = requests.post(url=configs.get("redis3").get("url") + uri_get, data=get_k,
                                        headers={'Content-Type': 'application/json;charset=utf-8'})
                    result_list = json.JSONDecoder().decode(res.text)["result"]
                    logger.info(
                        '删除成功=====用户为:"%s",删除的详细信息为:"%s","namespace":"%s", "key":"%s"' % (
                            username, redistype, namespace, keys) + "返回结果为：" + result_list)

                    return render_to_response('result.html', {"result_list": result_list, "keys": keys})
                else:
                    pool = redis.ConnectionPool(host=configs.get("redis2").get("host"),
                                                port=configs.get("redis2").get("port"),
                                                db=configs.get("redis2").get("db"))
                    rs = redis.StrictRedis(connection_pool=pool)
                    redis2keys = namespace + keys
                    try:
                        result_list = str(rs.delete(redis2keys))
                        logger.info(
                            '删除成功=====用户为:"%s",删除的详细信息为:"%s","namespace":"%s", "key":"%s"' % (
                                username, redistype, namespace, keys) + "返回结果为：" + result_list)
                    except BaseException, e:
                        logger.error(e)
                    return render_to_response('result.html', {"result_list": result_list, "keys": keys})
            else:
                error = form.errors
                logger.error(error)
                return render_to_response('error.html', {"error": error})
        else:
            form = nameSpaceForm()
