import time
from random import randint

from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import PhoneCode, User
from .serializers import PhoneRequestSerializer, PhoneVerifySerializer, ProfileSerializer, UseInviteSerializer


class RequestCodeView(GenericAPIView):
    serializer_class = PhoneRequestSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']

        code = f"{randint(0, 9999):04d}"
        PhoneCode.objects.create(phone_number=phone, code=code)

        time.sleep(1)
        return Response({'message': 'Код отправлен'}, status=status.HTTP_200_OK)


class VerifyCodeView(GenericAPIView):
    serializer_class = PhoneVerifySerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            phone_code = PhoneCode.objects.filter(phone_number=phone).latest('created_at')
        except PhoneCode.DoesNotExist:
            return Response({'message': 'Код не найден'}, status=status.HTTP_404_NOT_FOUND)

        if phone_code.is_expired() or phone_code.code != code:
            return Response({'message': 'Неверный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
                phone_number=phone,
                defaults={'username': phone}
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class ProfileAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class UseInviteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UseInviteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
