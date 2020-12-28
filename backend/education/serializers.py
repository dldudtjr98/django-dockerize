from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import (
    Curriculum, CurriculumStudent, Lecture, Lesson,
    CurriculumProgress, LectureDivision, CurriculumDivision
)


class CurriculumSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'password' in validated_data:  # patch password
            validated_data['password'] = make_password(validated_data['password'])
        curriculum = super().create(validated_data)
        return curriculum

    def update(self, instance, validated_data):
        if 'password' in validated_data:  # patch password
            validated_data['password'] = make_password(validated_data['password'])
        curriculum = super().update(instance, validated_data)
        return curriculum

    def validate(self, data):
        data = super().validate(data)
        if not data['public'] and 'password' not in data:
            raise serializers.ValidationError('공개 커리큘럼이 아니면, 비밀번호가 필요합니다.')
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError('시작일이 종료일보다 클 수 없습니다.')
        return data

    class Meta:
        model = Curriculum
        exclude = ['password', ]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture


class CurriculumDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumDivision
        fields = '__all__'


class CurriculumStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumStudent


class LectureDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureDivision


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson


class CurriculumProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumProgress
