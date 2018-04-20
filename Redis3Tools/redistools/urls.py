"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# -*- coding: UTF-8 -*-
from django.conf.urls import url

from . import search

urlpatterns = [
    url(r'^search-form/$', search.search_form),
    url(r'^search/$', search.search),
    url(r'^delete/$', search.delete),
    url(r'^login/$', search.login),
    url(r'^logout/$', search.logout),
    url(r'^', search.login),
]
