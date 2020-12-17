from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializers import CurriculumSerializer
from .models import Curriculum


class CurriculumView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Curriculum, pk=pk)

    def get(self, request, pk=None, format=None):
        if pk is None:
            curriculum_object = Curriculum.objects.all()
            serializer = CurriculumSerializer(curriculum_object, many=True)
        else:
            curriculum_object = self.get_object(pk)
            serializer = CurriculumSerializer(curriculum_object)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CurriculumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def patch(self, request, pk, format=None):
        curriculum_object = self.get_object(pk)
        serializer = CurriculumSerializer(curriculum_object, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def put(self, request, pk, format=None):
        curriculum_object = self.get_object(pk)
        serializer = CurriculumSerializer(curriculum_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, pk, format=None):
        curriculum_object = self.get_object(pk)
        curriculum_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
