# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import sys
import logging.handlers
from .sso_check import *;
import requests
import json, redis
from django.views.decorators.csrf import csrf_exempt
from .forms import nameSpaceForm
from .config_default import *
from imp import reload

reload(sys)
configs = configs
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
                        # print res.text
                        result_list = str(json.JSONDecoder().decode(res.text))
                        logger.info(
                            u'查询成功=====用户为:"%s",查询详细信息为:"%s","namespace":"%s", "key":"%s"' % (
                                username, redistype, namespace, keys) + u"返回结果为：" + result_list)
                        return render_to_response('result.html', {"result_list": result_list, "keys": keys})
                    except BaseException as e:
                        logger.error(e)
                        error = e
                    return render_to_response(('error.html', {"error": error}))
                else:
                    pool = redis.ConnectionPool(host=configs.get("redis2").get("host"),
                                                port=configs.get("redis2").get("port"),
                                                db=configs.get("redis2").get("db"))
                    rs = redis.StrictRedis(connection_pool=pool)
                    redis2keys = str(namespace + keys)
                    try:
                        result_list = rs.get(redis2keys)
                        aa = {"result_list": result_list, "keys": redis2keys}
                        logger.info(result_list)
                        logger.info(
                            u'查询成功=====用户为:"%s",查询详细信息为:"%s","namespace":"%s", "key":"%s"}' % (
                                username, redistype, namespace, keys) + u"返回结果为：" + aa)

                    except BaseException as e:
                        logger.error(e)
                        return render_to_response('error.html', {"error": e})
                    return render_to_response('result.html', {"result_list": aa, "keys": redis2keys})
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
                keys = form.cleaned_data['keys']
                logger.info(
                    '用户为:"%s",删除类型为:"%s","namespace":"%s", "key":"%s"}' % (username, redistype, namespace, keys))
                if (int(redistype) == 3):
                    uri_del = 'redis/v1/del'
                    get_k = '{"namespace":"%s", "key":"%s"}' % (namespace, keys)
                    res = requests.post(url=configs.get("redis3").get("url") + uri_del, data=get_k.encode('UTF-8'),
                                        headers={'Content-Type': 'application/json;charset=utf-8'})
                    result_list = str(json.JSONDecoder().decode(res.text))
                    logger.info(
                        '删除成功=====用户为:"%s",删除的详细信息为:"%s","namespace":"%s", "key":"%s"' % (
                            username, redistype, namespace, keys) + "返回结果为：" + result_list)

                    return render_to_response('result.html', {"result_list": result_list, "keys": keys})
                else:
                    pool = redis.ConnectionPool(host=configs.get("redis2").get("host"),
                                                port=configs.get("redis2").get("port"),
                                                db=configs.get("redis2").get("db"))
                    rs = redis.StrictRedis(connection_pool=pool)
                    redis2keys = str(namespace) + str(keys)
                    try:
                        result_list = str(rs.delete(redis2keys))
                        aa = {"result_list": result_list, "keys": redis2keys}
                        logger.info(
                            '删除成功=====用户为:"%s",删除的详细信息为:"%s","namespace":"%s", "key":"%s"' % (
                            username, redistype, namespace, keys) + u"返回结果为：" + aa)
                    except BaseException as e:
                        logger.error(e)
                    return render_to_response('result.html', {"result_list": aa, "keys": redis2keys})
            else:
                error = form.errors
                logger.error(error)
                return render_to_response('error.html', {"error": error})
        else:
            form = nameSpaceForm()
