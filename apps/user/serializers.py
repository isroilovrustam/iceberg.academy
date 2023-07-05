from django.contrib.auth import authenticate

from .models import User, Team, VerifyPhone
from rest_framework import serializers, exceptions


class VerifyPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPhone
        fields = ['phone', 'code']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'profession', 'name', 'image_path', 'bio']


class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['profession', 'name', 'image_path', 'bio']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone']

    def validate(self, attrs):
        phone = attrs['phone']
        if User.objects.filter(phone=phone):
            raise exceptions.AuthenticationFailed(
                {'success': False, 'message': "Telefon raqam oldin ro'yxatga olingan"})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password']

    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        tel = attrs['phone']
        pas = attrs['password']
        user = authenticate(phone=tel, password=pas)
        if not user:
            raise exceptions.AuthenticationFailed({'message': 'Telefon yoki parol xato'})
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password', 'password', 'conf_password']

    conf_password = serializers.CharField(min_length=8)
    old_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        pas1 = attrs['password']
        pas2 = attrs['conf_password']
        if not pas1 == pas2:
            raise exceptions.ValidationError(detail='Password did not match')
        return attrs


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone"]


class ForgetPasswordConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", 'password', 'conf_password']

    conf_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        phone = attrs['phone']
        pas1 = attrs['password']
        pas2 = attrs['conf_password']
        if pas1 != pas2:
            raise exceptions.ValidationError(detail='Passwordlar bir biriga mos kelmadi!')
        obj = User.objects.filter(phone=phone).first()
        obj.set_password(pas1)
        obj.save()
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'image_path', 'image', 'exercises', 'task_done', 'task_dont']

    image_path = serializers.CharField(read_only=True)
    image = serializers.FileField(write_only=True)
    exercises = serializers.SerializerMethodField(read_only=True)
    task_done = serializers.SerializerMethodField(read_only=True)
    task_dont = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_exercises(obj):
        if obj.user_courses.first():
            return sum([i.tasks.count() for i in obj.user_courses.first().course.lessons.all()])
        return 0

    @staticmethod
    def get_task_done(obj):
        count = 0
        if obj.user_courses.first():
            for i in obj.user_courses.first().course.lessons.all():
                for j in i.tasks.all():
                    for k in j.user_answers.all():
                        if k.status == 'Accepted':
                            count += 1
        return count

    @staticmethod
    def get_task_dont(obj):
        count = 0
        if obj.user_courses.first():
            for i in obj.user_courses.first().course.lessons.all():
                for j in i.tasks.all():
                    for k in j.user_answers.all():
                        if k.status != 'Accepted':
                            count += 1
        return count
