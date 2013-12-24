#-*-coding:utf-8-*-
__author__ = 'shenshen'

from django.conf.urls import patterns, url

from images import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^post_parameter$', views.post_parameter, name='post_parameter'),
    url(r'^get_parameter$', views.get_parameter, name='post_parameter'),
    url(r'^post_image$', views.post_image, name='post_image'),
    url(r'^get_image$', views.get_image, name='get_image'),
    url(r'^clear_database', views.clear_database, name='clear_database'),
    url(r'^test$', views.test, name='test'),
)
