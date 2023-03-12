#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   urls.py
@Time    :   2023/03/12
@Author  :   Junxiao Guo
@Version :   1.0
@License :   (C)Copyright 2022-2023, Junxiao Guo
@Desc    :   URL patterns for project view.
'''

from project import views
from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)


app_name = 'project'

urlpatterns = [
    path('', include(router.urls)),
]
