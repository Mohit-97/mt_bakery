from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        is_admin = validated_data.get('is_staff', False)

        if is_admin:
            user.is_active = False #admin user can only be allowed by superadmin
            user.save()

        return user
