from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .models import CustomUser, CustomGroup
from .serializers import CustomUserSerializer, CustomGroupSerializer


class UserView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CustomUser, pk=pk)

    def get(self, request, pk=None, format=None):
        if pk is None:
            user_object = CustomUser.objects.all()
            serializer = CustomUserSerializer(user_object, many=True)
        else:
            user_object = self.get_object(pk)
            serializer = CustomUserSerializer(user_object)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def patch(self, request, pk, format=None):
        user_object = self.get_object(pk)
        serializer = CustomUserSerializer(user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, pk, format=None):
        user_object = self.get_object(pk)
        user_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CustomGroup, pk=pk)

    def get(self, request, pk=None, format=None):
        if pk is None:
            group_object = CustomGroup.objects.all()
            serializer = CustomGroupSerializer(group_object, many=True)
        else:
            group_object = self.get_object(pk)
            serializer = CustomGroupSerializer(group_object)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def put(self, request, pk, format=None):
        group_object = self.get_object(pk)
        serializer = CustomGroupSerializer(group_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def patch(self, request, pk, format=None):
        group_object = self.get_object(pk)
        serializer = CustomGroupSerializer(group_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, pk, format=None):
        group_object = self.get_object(pk)
        group_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)