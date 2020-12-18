from django.test import TestCase
from django.conf import settings
from .models import CustomUser, CustomGroup
from .serializers import CustomUserSerializer


class CurriculumModelTest(TestCase):
    @classmethod
    def setUp(self):
        CustomGroup.objects.create(name=settings.DEFAULT_GROUP, description='')
        CustomGroup.objects.create(name='두번째그룹', description='')
        CustomGroup.objects.create(name='세번째그룹', description='')

        self.user = CustomUser.objects.create(
            id=2,
            password='1',
            user_id='testuser',
            email='dev@de1v.com',
            name='imtest',
        )
        self.user.set_password('123123')
        self.user.save()
        self.serialized_user = CustomUserSerializer(self.user).data

    def test_default_group(self):  # manytomany field인 group이 기본값으로 잘 설정되었는지
        self.assertEqual(self.serialized_user['group'][0]['name'], settings.DEFAULT_GROUP)
