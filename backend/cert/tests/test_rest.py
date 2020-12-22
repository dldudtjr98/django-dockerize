from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from cert.models import CustomUser, CustomGroup, UserGroup
from cert.serializers import CustomUserSerializer


class MemberTests(APITestCase):
    def setUp(self):
        self.first_group = CustomGroup.objects.create(name=settings.DEFAULT_GROUP, description='')
        self.second_group = CustomGroup.objects.create(name='랄라라', description='')
        self.adminuser = CustomUser.objects.create_superuser(  # auth를 위한 dummy admin 생성
            "admintest",
            "admintest@admintest.com",
            "admintest",
            "adminnick",
            "admintest"
        )
        self.user = CustomUser.objects.create(  # 중복테스트를 위한 user create
            password='1',
            user_id='testuser',
            email='dev@dev.com',
            name='imtest',
        )
        self.client.login(username='admintest', password='admintest')

    """
    CRUD 테스트
    POST(Create), POST(except parameter), GET(list), GET(retrive), PATCH, DELETE
    """
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
        self.assertEqual(CustomUser.objects.count(), 3)  # with superuser and setup user

    def test_create_member_no_name(self):
        url = reverse('member_without_pk')
        data = {
            'nickname': 'nicktest',
            'email': 'email@dev.com',
            'user_id': 'test_id',
            'password': 'dev1!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_member_no_nick(self):
        url = reverse('member_without_pk')
        data = {
            'name': 'testuser',
            'email': 'email@dev.com',
            'user_id': 'test_id',
            'password': 'dev1!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_member_no_email(self):
        url = reverse('member_without_pk')
        data = {
            'name': 'testuser',
            'nickname': 'nicktest',
            'user_id': 'test_id',
            'password': 'dev1!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_member_no_user_id(self):
        url = reverse('member_without_pk')
        data = {
            'name': 'testuser',
            'nickname': 'nicktest',
            'email': 'email@dev.com',
            'password': 'dev1!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_member_no_password(self):
        url = reverse('member_without_pk')
        data = {
            'name': 'testuser',
            'nickname': 'nicktest',
            'email': 'email@dev.com',
            'user_id': 'test_id',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_member_list(self):
        url = reverse('member_without_pk')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_member_detail(self):
        url = reverse('member_with_pk', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        serialized_user = CustomUserSerializer(self.user).data
        self.assertEqual(response.data, serialized_user)

    def test_patch_member_detail(self):
        url = reverse('member_with_pk', kwargs={'pk': self.user.id})
        data = {
            'name': 'testuserpatch',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.data['name'], 'testuserpatch')

    def test_delete_member_and_group_delete(self):  # delete 후에 manytomany argument 삭제 확인
        url = reverse('member_with_pk', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.usergroup = UserGroup.objects.filter(user_id=self.user.id).exists()
        self.assertFalse(self.usergroup)
