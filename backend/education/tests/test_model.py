from rest_framework.test import APITestCase
from .models import (
    Curriculum, CurriculumDivision, Lecture,
    LectureDivision, Lesson, CurriculumLecture,
    CurriculumStudent, CurriculumProgress,
)
from cert.models import CustomUser, CustomGroup


class EducationTests(APITestCase):
    """
    curriculum 분류를 만듬 (curriculum_div)
    curriculum을 만듬 (curriculum_one)
    curriculum을 하나 더 만듬 (curriculum_two)
    temp_curriculum을 만듬
    lecture 분류를 만듬 (lecture_div)
    lecture를 만듬 (lecture_one)
    lecture를 하나 더 만듬 (lecture_two)
    lesson을 만듬 (lesson_one)
    lesson을 하나 더 만듬 (lesson_two)
    student를 만듬 (member)
    """
    def setUp(self):
        self.curriculum_div_one = CurriculumDivision.objects.create(name="한컵 커리큘럼")
        self.curriculum_div_two = CurriculumDivision.objects.create(name="두컵 커리큘럼")
        self.curriculum_one = Curriculum.objects.create(
            title="커리큘럼 첫번째",
            password="1",
            division=self.curriculum_div_one.id,
            subject="이곳은 첫번째 커리큘럼의 주제이다.",
            disclosure=True,
            contents="이곳은 첫번째 커리큘럼의 내용이라고 할 수 있다.",
        )
        self.curriculum_two = Curriculum.objects.create(
            title="커리큘럼 두번째",
            password="1",
            division=self.curriculum_div_two.id,
            subject="이곳은 두번째 커리큘럼의 주제이다.",
            disclosure=True,
            contents="이곳은 두번째 커리큘럼의 내용이라고 할 수 있다.",
        )
        self.curriculum_one.set_password('123123')
        self.curriculum_two.set_password('456456')
        self.curriculum_one.save()
        self.curriculum_two.save()

        self.lecture_div_one = LectureDivision.objects.create(name="한컵 강의")
        self.lecture_div_two = LectureDivision.objects.create(name="두컵 강의")
        self.lecture_one = Lecture.objects.create(
            title="강의 첫번째",
            category=self.lecture_div_one.id,
            disclosure=True,
            contents="이곳은 첫번째 강의의 내용이라고 할 수 있다."
        )
        self.lecture_two = Lecture.objects.create(
            title="강의 두번째",
            category=self.lecture_div_two.id,
            disclosure=True,
            contents="이곳은 두번째 강의의 내용이라고 할 수 있다."
        )
        

    """
    테스트 시작

    -----------------------------------------------------------
    curriculum 시작날짜가 종료날짜보다 미래의 시간인지 확인
    curriculum 분류를 삭제하면 curriculum 사라지는지
    -----------------------------------------------------------
    lecture 분류를 삭제하면 lecture 사라지는지
    -----------------------------------------------------------
    lecture 삭제하면 lesson 사라지는지

    관계 table 확인
    -----------------------------------------------------------
    curriculum - student 관계 table

    curriculum 삭제
    student 삭제
    -----------------------------------------------------------
    curriculum - lecture 관계 table

    curriculum 삭제
    lecture 삭제
    curriculum 에 lecture 넣기
    lecture 시작시간이 종료시간보다 미래의 날짜인지 확인
    -----------------------------------------------------------
    student - curriculum - lecture - lesson table (curriculum 내 학생 학습률의 위한 table)

    lecture 삭제
    student 삭제
    curriculum 삭제
    lesson 삭제
    """
