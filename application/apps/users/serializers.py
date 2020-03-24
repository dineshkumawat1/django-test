from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.users.models import User, UserProfile
from django.contrib.auth.models import Group
from django.db.models import Q
import re
from config import settings
from django.utils import timezone
from django.utils.timezone import now


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        is_active = 1 if user.is_active == True else 0
        # serializer = UserDetailSerializer(user)
        # token['data'] = serializer.data

        token['email'] = user.email
        token['name'] = user.name
        token['is_active'] = is_active
        token['global_login_token'] = user.is_active

        return token


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60, required=True)
    username = serializers.CharField(max_length=60, required=True)
    mobile = serializers.CharField(max_length=20, required=True)
    email = serializers.CharField(validators=[validate_email], required=True)
    password = serializers.CharField(max_length=45, required=True, write_only=True)
    confirm_password = serializers.CharField(max_length=45, required=True)

    class Meta:
        extra_kwargs = {'confirm_password'}

    def validate_name(self, name):
        if name is None or len(name) < 3:
            raise serializers.ValidationError('Name should be least 3 characters long.')
        elif len(name) > 40:
            raise serializers.ValidationError('Name should be below 40 characters.')
        elif not re.match(r"^[ a-zA-Z0-9_.-]*$", name):
            raise serializers.ValidationError('Allowed characters [a-z] and [A-Z] and [0-9] and [-, ., _')
        return name

    def validate_username(self, value):
        """
        Validates email address
        :param value:
        :return: email as value if no exception raised
        """
        if not value:
            raise serializers.ValidationError('username is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(username=value).exists():
                    return value
                else:
                    raise serializers.ValidationError('username should be unique')
            except Exception as error:
                raise error

    def validate_mobile(self, mobile):
        """
        Validates mobile no, if value(mobile_no) is not None
        Then it tries to find the user with this mobile no
        if it finds that mobile no is registered it raises
        the exception that no is registered, otherwise returns
        mobile_no as value
        :param value:
        :return: value if no exception raised
        """
        # test_mobile = None
        test_mobile = mobile
        # test_mobile = re.split("( )", mobile)  # mobile should be like +91 9771020304
        # test_mobile = test_mobile[2]

        if not test_mobile:
            raise serializers.ValidationError('Mobile no is required.')
        elif len(test_mobile)!= 10:
            raise serializers.ValidationError('Mobile number must be of 10 digits')
        elif not test_mobile.isdigit():
            raise serializers.ValidationError('Only digits are allowed for mobile')
        else:
            try:
                User = get_user_model()
                if not self.instance:
                    user = User.objects.get(mobile=mobile)
                else:
                    user = User.objects.get(~Q(id=self.instance.id), mobile=mobile)
                raise serializers.ValidationError('Mobile no is already registered.')
            except User.DoesNotExist:
                return mobile
            except Exception as error:
                raise error

    def validate_email(self, value):
        """
        Validates email address
        :param value:
        :return: email as value if no exception raised
        """
        if not value:
            raise serializers.ValidationError('email is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(email=value).exists():
                    return value
                else:
                    raise serializers.ValidationError('email id is already registered.')
            except Exception as error:
                raise error



    def validate_password(self, value):
        """
        Validates password
        :param value:
        :return: password as value if no exception raised
        """
        return value



    def validate(self, data):
        """
        Check that password must be equal to confirm password.
        """
        # confirm_password = data.pop('confirm_password')
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and Confirm password does not match")
        if 'device_type' not in data:
            data['device_type'] = 'website'

        data.pop('confirm_password')

        return data

    def create(self, validated_data):
        """
        Register new user with validated_data
        :param validated_data:
        :return: Newly created user object
        """
        validated_data.pop('confirm_password', None)
        try:
            validated_data['username'] = validated_data['username']
            validated_data['name'] = validated_data['name']
            validated_data['email'] = validated_data['email']
            validated_data['mobile'] = validated_data['mobile']
            validated_data['password'] = make_password(validated_data['password'])
            validated_data['is_staff'] = 0
            validated_data['is_superuser'] = 0
            # validated_data['created_on'] = timezone.now()
            # validated_data['updated_on'] = now
            validated_data['global_login_token'] = get_unique_id()
            validated_data['device_type'] = validated_data['device_type'] or 'website'
            # with transaction.atomic():
            #     validated_data.pop('confirm_password', None)
            #     print('++++++NEW VALIDATED DATA+++++++++++++')
            #     print(validated_data)
            #     user = get_user_model().objects.create(**validated_data)
            #     if user:
            #         print('User created/*/*/*/*/*/*/********************************')
            #         user.create_profile()
            user = validated_data

        except Exception as e:
            raise e
        return user


class UserProfileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'mobile', 'profile_pic', 'profile']

    def get_profile(self, obj):
        user_prof = UserProfile.objects.get(user=obj)
        prof_ser = UserProfileDetailSerializer(user_prof)
        return prof_ser.data


class SocialUserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60, required=True)
    username = serializers.CharField(max_length=60, required=True)
    # mobile = serializers.CharField(max_length=20, required=True)
    email = serializers.CharField(validators=[validate_email], required=True)
    password = serializers.CharField(max_length=255, min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(max_length=255, min_length=8, required=True)

    class Meta:
        extra_kwargs = {'confirm_password'}

    def validate_email(self, value):
        """
        Validates email address
        :param value:
        :return: email as value if no exception raised
        """
        if not value:
            raise serializers.ValidationError('email is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(email=value).exists():
                    return value
                else:
                    raise serializers.ValidationError('email id is already registered.')
            except Exception as error:
                raise error

    def validate_username(self, value):
        """
        Validates email address
        :param value:
        :return: email as value if no exception raised
        """
        if not value:
            raise serializers.ValidationError('email is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(username=value).exists():
                    return value
                else:
                    raise serializers.ValidationError('email id is already registered.')
            except Exception as error:
                raise error

    def validate_name(self, name):
        if name is None or len(name) < 3:
            raise serializers.ValidationError('Required at least 3 characters long.')
        elif len(name) > 40:
            raise serializers.ValidationError('Name should be below 40 characters.')
        elif not re.match(r"^[ a-zA-Z0-9_.-]*$", name):
            raise serializers.ValidationError('Allowed characters [a-z] and [A-Z] and [0-9] and [-, ., _')
        return name

    def validate(self, data):
        """
        Check that password must be equal to confirm password.
        """
        # confirm_password = data.pop('confirm_password')
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password and confirm password does not match")
        if 'device_type' not in data:
            data['device_type'] = 'website'

        data.pop('confirm_password')

        return data

    def create(self, validated_data):
        """
        Register new user with validated_data
        :param validated_data:
        :return: Newly created user object
        """
        validated_data.pop('confirm_password', None)
        try:
            validated_data['username'] = validated_data['username']
            validated_data['name'] = validated_data['name']
            validated_data['email'] = validated_data['email']
            validated_data['password'] = make_password(validated_data['password'])
            validated_data['is_staff'] = 0
            validated_data['is_superuser'] = 0
            # validated_data['created_on'] = timezone.now()
            # validated_data['updated_on'] = now
            validated_data['global_login_token'] = get_unique_id()
            validated_data['device_type'] = validated_data['device_type'] or 'website'
            # with transaction.atomic():
            #     validated_data.pop('confirm_password', None)
            #     print('++++++NEW VALIDATED DATA+++++++++++++')
            #     print(validated_data)
            #     user = get_user_model().objects.create(**validated_data)
            #     if user:
            #         print('User created/*/*/*/*/*/*/********************************')
            #         user.create_profile()
            user = validated_data

        except Exception as e:
            raise e
        return user


