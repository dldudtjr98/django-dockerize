from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from education.models import (
    Curriculum, CurriculumDivision, Lecture,
    LectureDivision, Lesson, CurriculumLecture,
    CurriculumStudent, CurriculumProgress
)
from education.serializers import CurriculumSerializer, CurriculumStudentSerializer, LectureSerializer
from cert.models import CustomUser


class EducationRestTests(APITestCase):
    def setUp(self):
        self.adminuser = CustomUser.objects.create_superuser(  # auth를 위한 dummy admin 생성
            "admintest",
            "admintest@admintest.com",
            "admintest",
            "adminnick",
            "admintest"
        )
        self.student_one = CustomUser.objects.create(
            password='1',
            user_id='testuser',
            email='dev@dev.com',
            name='imtest',
        )
        self.student_two = CustomUser.objects.create(
            password='1',
            user_id='testuser2',
            email='dev2@dev.com',
            name='imtest2',
        )
        self.client.login(username='admintest', password='admintest')
        self.curriculum_div_one = CurriculumDivision.objects.create(name='한컵 커리')
        self.curriculum_div_two = CurriculumDivision.objects.create(name='두컵 커리')
        self.curriculum_one = Curriculum.objects.create(
            title="커리큘럼 첫번째",
            password="1",
            division=self.curriculum_div_one.id,
            subject="이곳은 첫번째 커리큘럼의 주제이다.",
            public=True,
            contents="이곳은 첫번째 커리큘럼의 내용이라고 할 수 있다.",
            start_date="2020-12-22 10:00:00",
            end_date="2021-02-22 10:00:00"
        )
        self.curriculum_two = Curriculum.objects.create(
            title="커리큘럼 두번째",
            password="1",
            division=self.curriculum_div_two.id,
            subject="이곳은 두번째 커리큘럼의 주제이다.",
            public=True,
            contents="이곳은 두번째 커리큘럼의 내용이라고 할 수 있다.",
            start_date="2020-12-22 10:00:00",
            end_date="2021-02-22 10:00:00"
        )
        self.lecture_div_one = LectureDivision.objects.create(name="한컵 강의")
        self.lecture_div_two = LectureDivision.objects.create(name="두컵 강의")
        self.lecture_one = Lecture.objects.create(
            title="강좌 첫번째",
            category=self.lecture_div_one.id,
            difficult="심화",
            public=True,
            contents="이곳은 첫번째 강좌의 내용이라고 할 수 있다."
        )
        self.lecture_two = Lecture.objects.create(
            title="강좌 두번째",
            category=self.lecture_div_two.id,
            difficult="기초",
            public=True,
            contents="이곳은 두번째 강좌의 내용이라고 할 수 있다."
        )
        self.curriculum_one.students.add(self.student_one.id)
        self.curriculum_one.students.add(self.student_two.id)
        CurriculumLecture.objects.create(
            curriculum_id=self.curriculum_one.id,
            lecture_id=self.lecture_one.id,
            start_date='2020-12-22 00:00:00',
            end_date='2020-12-31 00:00:00',
            ordering=1,
        )
        CurriculumLecture.objects.create(
            curriculum_id=self.curriculum_one.id,
            lecture_id=self.lecture_two.id,
            start_date='2020-12-22 00:00:00',
            end_date='2020-12-31 00:00:00',
            ordering=2,
        )

    """
    -------------------------------------------------------------------------
    CURRICULUM POST TEST
    -------------------------------------------------------------------------
    """
    def test_create_curriculum(self):  # 정상 parameter curriculum
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2020-12-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curriculum.objects.count(), 3)

    def test_create_curriculum_no_password_but_public(self):  # 공개 curriculum
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': True,
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2020-12-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curriculum.objects.count(), 3)

    def test_create_curriculum_no_title(self):  # title parameter 없음
        url = reverse('curriculum_without_pk')
        data = {
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2020-12-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curriculum_no_subject(self):  # subject parameter 없음
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2020-12-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curriculum_no_div(self):  # division parameter 없음
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2020-12-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curriculum_no_start_date(self):  # start_date parameter 없음
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curriculum_no_end_date(self):  # end_date parameter 없음
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2020-12-22 10:00:00',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curriculum_start_bigger_than_end(self):  # 시작일이 종료일보다 큼
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'password': '123123',
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2021-03-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_curriculum_private_but_no_password(self):  # 비공개지만 패스워드가 없음
        url = reverse('curriculum_without_pk')
        data = {
            'title': '첫번째 커리큘럼 테스트',
            'division': self.curriculum_div_one.id,
            'subject': '첫번째 커리큘럼 테스트의 주제입니다. 안녕하세요',
            'public': False,
            'contents': '첫번째 커리큘럼의 내용입니다. 안녕안녕안녕안녕하세요요요요요',
            'start_date': '2021-03-22 10:00:00',
            'end_date': '2021-01-11 10:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    -------------------------------------------------------------------------
    CURRICULUM GET TEST
    -------------------------------------------------------------------------
    """
    def test_get_curriculum_list(self):
        url = reverse('curriculum_without_pk')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_get_curriculum_detail(self):
        url = reverse('curriculum_with_pk')
        response = self.client.get(url, kwargs={'pk': self.curriculum_one.id})
        serialized_curriculum = CurriculumSerializer(self.curriculum_one).data
        self.assertEqual(response.data, serialized_curriculum)

    def test_curriculum_student(self):
        url = reverse('curriculum_member')
        response = self.client.get(url, kwargs={'curriculum_id': self.curriculum_one.id})
        serialized_curriculum_students = CurriculumStudentSerializer(self.curriculum_one.students).data
        self.assertEqual(response.data, serialized_curriculum_students)

    """
    -------------------------------------------------------------------------
    CURRICULUM PATCH TEST
    -------------------------------------------------------------------------
    """
    def test_curriculum_patch(self):
        url = reverse('curriculum_with_pk', kwargs={'pk': self.curriculum_one.id})
        title_data = {
            'title': '제목을 바꿔볼까요?'
        }
        response = self.client.patch(url, title_data, format='json')
        self.assertEqual(response.data['title'], '제목을 바꿔볼까요?')

        division_data = {
            'division': self.curriculum_div_two.id
        }
        response = self.client.patch(url, division_data, format='json')
        self.assertEqual(response.data['division']['id'], self.curriculum_div_two.id)

        subject_data = {
            'subject': '주제를 바꿔볼까요?'
        }
        response = self.client.patch(url, subject_data, format='json')
        self.assertEqual(response.data['subject'], '주제를 바꿔볼까요?')

    """
    -------------------------------------------------------------------------
    CURRICULUM DELETE TEST
    -------------------------------------------------------------------------
    """
    def test_curriculum_delete(self):  # curriculum 삭제 시 curriculum-student, curriculum-lecture args 확인
        url = reverse('curriculum_with_pk', kwargs={'pk': self.curriculum_one.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CurriculumStudent.objects.filter(curriculum_id=self.curriculum_one.id).exists())
        self.assertFalse(CurriculumLecture.objects.filter(curriculum_id=self.curriculum_one.id).exists())

    def test_curriculum_delete_student(self):  # student 삭제 시 curriculum-student args 확인
        url = reverse('member_with_pk', kwargs={'pk': self.student_one.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CurriculumStudent.objects.filter(user_id=self.student_one.id).exists())

    def test_curriculum_delete_lecture(self):  # lecture 삭제 시 curriculum-lecture args 확인
        url = reverse('lecture_with_pk', kwargs={'pk': self.lecture_one.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CurriculumLecture.objects.filter(lecture_id=self.lecture_one.id).exists())

    def test_curriculum_leave_student(self):  # student 탈퇴 시 curriculum-student args 확인
        url = reverse('curriculum_member_with_pk', kwargs={
            'curriculum_id': self.curriculum_one.id,
            'user_id': self.student_one.id
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CurriculumStudent.objects.filter(user_id=self.student_one.id).exists())

    def test_curriculum_discharge_lecture(self):  # lecture 비할당 시 curriculum-lecture args 확인
        url = reverse('curriculum_lecture_with_pk', kwargs={
            'curriculum_id': self.curriculum_one.id,
            'lecture_id': self.lecture_one.id
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CurriculumLecture.objects.filter(user_id=self.lecture_one.id).exists())

    """
    -------------------------------------------------------------------------
    LECTURE POST TEST (CURRICULUM-LECTURE)
    -------------------------------------------------------------------------
    """
    def test_create_lecture(self):  # 정상 parameter lecture
        url = reverse('lecture_without_pk')
        data = {
            'title': '첫번째 lecture 테스트',
            'division': self.lecture_div_one.id,
            'difficulty': 'Basic',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lecture.objects.count(), 3)

    def test_create_lecture_no_title(self):  # title parameter 없음
        url = reverse('lecture_without_pk')
        data = {
            'division': self.lecture_div_one.id,
            'difficulty': 'Basic',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lecture_no_div(self):  # division parameter 없음
        url = reverse('lecture_without_pk')
        data = {
            'title': '첫번째 lecture 테스트',
            'difficulty': 'Basic',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lecture_no_difficulty(self):  # difficulty parameter 없음
        url = reverse('lecture_without_pk')
        data = {
            'title': '첫번째 lecture 테스트',
            'division': self.lecture_div_one.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_curriculum_charge_lecture(self):
        url = reverse('curriculum_lecture_without_pk')
        data = {
            'curriculum_id': self.curriculum_two.id,
            'lecture_id': self.lecture_one.id,
            'start_date': '2020-12-22 00:00:00',
            'end_date': '2020-12-31 00:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_curriculum_charge_lecture_future_date(self):  # lecture start date가 end date보다 뒤
        url = reverse('curriculum_lecture_without_pk')
        data = {
            'curriculum_id': self.curriculum_two.id,
            'lecture_id': self.lecture_one.id,
            'start_date': '2020-12-31 00:00:00',
            'end_date': '2020-12-22 00:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_curriculum_charge_lecture_no_end_date(self):  # lecture start date가 end date보다 뒤
        url = reverse('curriculum_lecture_without_pk')
        data = {
            'curriculum_id': self.curriculum_two.id,
            'lecture_id': self.lecture_one.id,
            'start_date': '2020-12-31 00:00:00',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_curriculum_charge_lecture_no_start_date(self):  # lecture start date가 end date보다 뒤
        url = reverse('curriculum_lecture_without_pk')
        data = {
            'curriculum_id': self.curriculum_two.id,
            'lecture_id': self.lecture_one.id,
            'end_date': '2020-12-22 00:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_curriculum_charge_lecture_no_curriculum(self):  # lecture start date가 end date보다 뒤
        url = reverse('curriculum_lecture_without_pk')
        data = {
            'lecture_id': self.lecture_one.id,
            'start_date': '2020-12-22 00:00:00',
            'end_date': '2020-12-31 00:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_curriculum_charge_lecture_no_lecture(self):
        url = reverse('curriculum_lecture_without_pk')
        data = {
            'curriculum_id': self.curriculum_two.id,
            'start_date': '2020-12-22 00:00:00',
            'end_date': '2020-12-31 00:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    -------------------------------------------------------------------------
    LECTURE GET TEST (CURRICULUM-LECTURE)
    -------------------------------------------------------------------------
    """
    def test_lecture_list(self):
        url = reverse('lecture_without_pk')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_lecture_detail(self):
        url = reverse('lecture_with_pk')
        response = self.client.get(url, kwargs={'pk': self.lecture_one.id})
        serialized_lecture = LectureSerializer(self.lecture_one).data
        self.assertEqual(response.status_data, serialized_lecture)

    def test_lecture_lesson(self):
        url = reverse('lecture_with_pk')
        response = self.client.get(url, kwargs={'pk': self.lecture_one.id})