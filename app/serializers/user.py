from rest_framework import serializers
from models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['is_superuser','is_staff','groups','user_permissions','last_login']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(**validated_data)
        if user.is_superuser is True:
            user.is_staff = True
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance