#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   views.py
@Time    :   2023/03/12
@Author  :   Junxiao Guo
@Version :   1.0
@License :   (C)Copyright 2022-2023, Junxiao Guo
@Desc    :   Views for the Project APIs
'''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Project
from project import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage Project APIs."""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new project."""
        serializer.save(manager=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ProjectSerializer
        return self.serializer_class
