#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   serializers.py
@Time    :   2023/03/12
@Author  :   Junxiao Guo
@Version :   1.0
@License :   (C)Copyright 2022-2023, Junxiao Guo
@Desc    :   Serializers for projects
'''

from rest_framework import serializers
from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for experience."""

    class Meta:
        model = Project
        fields = ['title', 'description', 'manager']
        read_only_fields = ['manager']

    def create(self, validated_data):
        """Create a experience."""
        title = validated_data.pop('title')
        description = validated_data.pop('description')
        project, _ = Project.objects.update_or_create(
            title=title, description=description, defaults=validated_data)

        return project
