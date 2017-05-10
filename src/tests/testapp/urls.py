# -*- coding: utf-8 -*-
"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from tests.testapp.views import TransExampleView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="l10n_extensions/testapp/home.html"),
        name="home"),
    url(r'^login/$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^translate_example/', TransExampleView.as_view(template_name="l10n_extensions/testapp/translate_example.html"),
        name="translate example"),
    url(r'^i18n/',include('django.conf.urls.i18n')),
]
