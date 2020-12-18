from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, CustomGroup


class MemberTests(APITestCase):
    def setUp(self):
        CustomGroup.objects.create(name=settings.DEFAULT_GROUP, description='')
        self.user = CustomUser.objects.create_superuser(  # auth를 위한 dummy admin 생성
                "admintest",
                "admintest@admintest.com",
                "admintest",
                "adminnick",
                "admintest"
            )
        self.client.login(username='admintest', password='admintest')

    def test_create_member(self):
        url = reverse('member_without_pk')
        data = {
            'name': 'testuser',
            'nickname': 'nicktest',
            'email': 'email@dev.com',
            'user_id': 'test_id',
            'password': 'dev1!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # with superuser
