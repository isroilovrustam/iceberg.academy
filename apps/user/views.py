from random import randint
from rest_framework import generics, response, status, permissions, views
from .models import Team, User, VerifyPhone
from .serializers import TeamSerializer, UserRegisterSerializer, LoginSerializer, VerifyPhoneSerializer, \
    ForgetPasswordSerializer, ForgetPasswordConfirmSerializer, UserSerializer, ChangePasswordSerializer, \
    TeamDetailSerializer
from .utils import verify
from rest_framework.authtoken.models import Token


class TeamAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailAPI(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        phone = self.request.data['phone']
        pas1 = self.request.data['password']
        pas2 = self.request.data['conf_password']
        if pas1 != pas2:
            return response.Response({'success': False, 'message': "Passwords did not match"})
        code = str(randint(1000, 10000))
        verify(phone, code)
        VerifyPhone.objects.create(phone=phone, code=code)
        serializer.save()
        user = User.objects.filter(phone=phone).first()
        user.set_password(pas1)
        user.save()
        Token.objects.create(user=user)
        return response.Response({"success": True, 'message': "Telefon raqamga tasdiqlash kodi yuborildi!!!"},
                                 status=status.HTTP_201_CREATED)


class VerifyPhoneAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = VerifyPhoneSerializer

    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        code = self.request.data['code']
        v = VerifyPhone.objects.filter(phone=phone, code=code).first()
        if v:
            v.delete()
        else:
            return response.Response({'message': "Tasdiqlash kodi xato kiritildi!"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(phone=phone).first()
        user.is_active = True
        user.save()
        user_serializer = UserSerializer(instance=user).data
        token = Token.objects.get(user=user)
        user_serializer['token'] = token.key
        return response.Response({'success': True, 'result': user_serializer})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        phone = self.request.data['phone']
        user = User.objects.filter(phone=phone).first()
        token = Token.objects.get(user=user)
        return response.Response({"token": token.key})


class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        old_password = self.request.data['old_password']
        password = self.request.data['password']
        user = self.request.user
        if not user.check_password(old_password):
            return response.Response({"message": "Oldinggi parolingiz xato kiritildi "},
                                     status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return response.Response({"message": "Parolingiz yangilandi "})


class ForgetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        phone = self.request.data["phone"]
        code = str(randint(1000, 10000))
        verify(phone, code)
        VerifyPhone.objects.create(phone=phone, code=code)
        return response.Response({"message": "Code yuborildi "})


class VerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyPhoneSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        code = self.request.data['code']
        v = VerifyPhone.objects.filter(phone=phone, code=code).first()
        if v:
            v.delete()
        else:
            return response.Response({'message': "Tasdiqlash kodi xato kiritildi!"}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({"message": "Parolini kiriting "})


class ForgetPasswordConfirmAPIView(generics.GenericAPIView):
    serializer_class = ForgetPasswordConfirmSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response({"message": "Parolingiz tiklandi"})


class UserAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(instance=user, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(instance=user)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return response.Response({'success': True})
