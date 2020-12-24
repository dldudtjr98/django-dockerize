from rest_framework import serializers
from .models import (
    Curriculum, CurriculumStudent, Lecture, Lesson,
    CurriculumProgress, LectureDivision, CurriculumDivision
)


class CurriculumSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        curriculum = super().create(validated_data)
        curriculum.set_password(validated_data['password'])
        curriculum.save()
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


class LectureDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureDivision


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson


class CurriculumProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumProgress
