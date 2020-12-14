from rest_framework import serializers
from account.models import CustomUser


class CustomUserReadSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {"password" : {"write_only" : True}} # password always write_only

class CustomUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = CustomUser(
            email = validated_data['email'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validate_data):
        user = super().update(instance, validate_data)
        if 'password' in validate_data: # patch password
            user.set_password(validate_data['password'])
        user.save()
        return user
        
    class Meta:
        model = CustomUser
        exclude = ['is_admin', 'last_login',]
        extra_kwargs = {"password" : {"write_only" : True}}