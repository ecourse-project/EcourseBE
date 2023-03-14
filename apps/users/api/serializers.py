from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from apps.users.models import User, UserResetPassword
from apps.users.exceptions import (
    OldPasswordNotCorrectException,
    PasswordNotMatchException,
)
from apps.carts.models import Cart, FavoriteList


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "avatar",
            "phone",
        )

    @classmethod
    def get_avatar(cls, obj):
        return obj.get_avatar()

    # def update(self, instance, validated_data):
    #     print(instance.avatar)
    #     print(validated_data)
    #     validated_data['first_name'] = self.initial_data.get('first_name', "")
    #     # last_name = self.initial_data.get('last_name', "")
    #     print(self.initial_data)
    #     return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise PasswordNotMatchException
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise OldPasswordNotCorrectException
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        UserResetPassword.objects.filter(email=instance.email).update(is_changed=True)
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'full_name',
            )
        extra_kwargs = {
            'full_name': {'required': True},
            }
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"Message": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
        )
        user.set_password(validated_data['password1'])
        user.save(update_fields=['password'])

        Cart.objects.create(user=user)
        FavoriteList.objects.create(user=user)
        return user

    