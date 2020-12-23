from rest_framework import serializers
from .models import (
    Curriculum, CurriculumDivision, CurriculumStudent,
    Lecture, Lesson
)


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'


class CurriculumDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumDivision
        fields = '__all__'


class CurriculumStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumStudent


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
