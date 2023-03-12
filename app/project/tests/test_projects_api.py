#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   test_projects_api.py
@Time    :   2023/03/12
@Author  :   Junxiao Guo
@Version :   1.0
@License :   (C)Copyright 2022-2023, Junxiao Guo
@Desc    :   Tests for projects API
'''

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project

from project.serializers import ProjectSerializer

PROJECT_URL = reverse('project:project-list')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_project(user, **params):
    """Create and return a sample experience."""
    defaults = {
        'title': params.get('title', 'Example Project'),
        'description': params.get('description',
                                  'description for example project.'),
    }
    defaults.update(params)

    project, _ = Project.objects.update_or_create(manager=user, **defaults)
    project.members.add(user)
    return project


class PublicProjectAPITest(TestCase):
    """Test unauthorized API request."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PROJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExperienceAPITest(TestCase):
    """Test authorized API requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_experiences(self):
        """Test retrieving a list of experiences."""
        create_project(user=self.user)
        create_project(user=self.user)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_blog_list_available_to_users(self):
        """Test list of experiences is available to authenticated users."""
        other_user = create_user(email='other@example.com', password='test123')
        create_project(user=other_user, title='Test project1',
                       description="Description for test project1.")
        create_project(user=self.user, title='Test project2',
                       description='Test description for project2.')

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
