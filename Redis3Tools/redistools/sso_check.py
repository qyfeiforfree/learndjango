# -*- coding: utf-8 -*-
import requests
from django.shortcuts import HttpResponseRedirect

SSO_URL = "http://sso.XXX.com/sso"


def sso_check(func):
    def _wrap(request, *args, **kwargs):
        # 判断session 是否有效
        SSO_LOGIN_URL = "%s?back=%s" % (SSO_URL + "/login", request.build_absolute_uri())
        SSO_COOKIE_URL = "%s?back=%s" % (SSO_URL + "/cookie", request.build_absolute_uri())
        # 通过session检查用户是否登陆
        cookie_status = requests.get(SSO_COOKIE_URL, cookies=request.COOKIES, allow_redirects=True).json()
        if not cookie_status["status"]:
            return HttpResponseRedirect(SSO_LOGIN_URL)
        return func(request, *args, **kwargs)

    return _wrap


def getuser(request):
    url = SSO_URL + "/user"
    userinfo = requests.get(url, cookies=request.COOKIES, allow_redirects=True).json()
    return userinfo
