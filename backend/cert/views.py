from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .models import CustomUser, CustomGroup, UserGroup
from .serializers import (
    CustomUserSerializer, CustomGroupSerializer, UserGroupSerializer,
    LoginUserSerializer, CreateUserSerializer
)


class UserView(APIView):
    """
        Member API

        ---
    """
    def del_user_all_group(self, pk):
        group = UserGroup.objects.filter(user_id=pk)
        group.delete()

    def data_to_validate(self, groups, pk):
        validated_data = []
        for group in groups:
            user_group = {"group": group, "user": pk}
            validated_data.append(user_group)
        return validated_data

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
            return Response({
                'user': serializer.data
            })
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def patch(self, request, pk, format=None):
        user_object = self.get_object(pk)
        serializer = CustomUserSerializer(user_object, data=request.data, partial=True)

        if 'groups' in request.data:
            self.del_user_all_group(pk)
            user_group_data = self.data_to_validate(request.data['groups'], pk)
            usergroup_serializer = UserGroupSerializer(data=user_group_data, many=True)
            if serializer.is_valid() and usergroup_serializer.is_valid():
                usergroup_serializer.save()  # cause if user doesn't have group, has DEFAULT GROUP
                serializer.save()
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        else:
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


class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                'user': serializer.data['user_id'],
                'token': AuthToken.objects.create(user)[1],
            })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
            })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
