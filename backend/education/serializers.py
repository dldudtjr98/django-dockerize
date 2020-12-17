from rest_framework import serializers
from .models import Curriculum, CurriculumDivision


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'


class CurriculumDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumDivision
        fields = '__all__'
