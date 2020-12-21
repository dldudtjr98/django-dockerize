from django.test import TestCase
from django.conf import settings
from .models import (
    Curriculum, CurriculumDivision, Lecture,
    LectureDivision, Lesson, CurriculumLecture,
    CurriculumStudent, CurriculumProgress,
)
from cert.models import CustomUser, CustomGroup


class EducationTests(APITestCase):
    """
    curriculum을 만듬 (curriculum_one)
    curriculum을 하나 더 만듬 (curriculum_two)
    curriculum 분류를 만듬 (curriculum_div)
    lecture를 만듬 (lecture_one)
    lecture를 하나 더 만듬 (lecture_two)
    lecture 분류를 만듬 (lecture_div)
    lesson을 만듬 (lesson_one)
    lesson을 하나 더 만듬 (lesson_two)
    student를 만듬 (member)
    """
    def setUp(self):
        

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