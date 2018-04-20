# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import os, logging, datetime, pytz
from django.forms.models import model_to_dict

import json
from sso_check import *


def login(request):
    SSO_URL = "http://sso.qm.qianbao-inc.com/sso"
    SSO_LOGIN_URL = "%s?back=%s" % (SSO_URL + "/login", 'http://%s/' % request.get_host())
    # 通过session检查用户是否登陆
    return HttpResponseRedirect(SSO_LOGIN_URL + "redistools/search-form/")


def logout(request):
    SSO_URL = "http://sso.qm.qianbao-inc.com/sso"
    SSO_LOGIN_URL = "%s?back=%s" % (SSO_URL + "/logout", 'http://%s/' % request.get_host())
    # 通过session检查用户是否登陆
    return HttpResponseRedirect(SSO_LOGIN_URL + "redistools/search-form/")
