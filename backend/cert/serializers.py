from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, CustomGroup, UserGroup


class CustomGroupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        group = CustomGroup(
            name=validated_data['name'],
            description=validated_data['description']
        )
        group.save()
        return group

    def update(self, instance, validated_data):
        group = super().update(instance, validated_data)
        group.save()
        return group

    class Meta:
        model = CustomGroup
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_group = UserGroup(
            group=validated_data['group'],
            user=validated_data['user']
        )
        user_group.save()
        return user_group

    class Meta:
        model = UserGroup
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    group = CustomGroupSerializer(read_only=True, many=True)

    def create(self, validated_data):
        user = CustomUser(
            user_id=validated_data['user_id'],
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        if 'password' in validated_data:  # patch password
            user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        exclude = ['is_admin', 'is_staff']
        extra_kwargs = {"password": {"write_only": True}}


class LoginUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('인증/활성화 되지 않은 사용자입니다.')


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = CustomUser(
            user_id=validated_data['user_id'],
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ("id", "user_id", "password", "name", "nickname", "email")
        extra_kwargs = {"password": {"write_only": True}}
