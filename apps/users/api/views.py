from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.api.serializers import (
    UserSerializer,
    ChangePasswordSerializer,
)
from apps.users.exceptions import UserNotExistException
from apps.users import services
from apps.users.models import User
from apps.users.choices import STUDENT
from django.conf import settings
from django.core.mail import send_mail
from apps.users.choices import (
    PASSWORD_RESET_EMAIL_TITLE,
    PASSWORD_RESET_EMAIL_MESSAGE,
)
from apps.core.utils import id_generator


class UserInfoView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.request.query_params.get("user_id")
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise UserNotExistException
        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        user = self.request.user
        if not user.is_anonymous and user.role == STUDENT:
            data.pop("phone")
        return Response(data)


class UsersProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class UserExistView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        exists = services.exists_user(email=email)
        data = {"exists": exists}
        return Response(data, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        email = data.get('email', None)
        if not email:
            return Response({"detail": "Email is required!"}, status=status.HTTP_204_NO_CONTENT)

        user = User.objects.filter(email=email).first()
        if not user:
            raise UserNotExistException

        new_password = id_generator()
        user.set_password(new_password)
        user.save(update_fields=["password"])
        send_mail(
                    PASSWORD_RESET_EMAIL_TITLE,
                    PASSWORD_RESET_EMAIL_MESSAGE + new_password,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
        return Response({"detail": "Please, check your email!"}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.RetrieveUpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"detail": "Password has been changed!"}, status=status.HTTP_200_OK)
