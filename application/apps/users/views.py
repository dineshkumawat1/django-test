from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import coreapi
import coreschema
from .serializers import UserCreateSerializer, UserDetailsSerializer, SocialUserCreateSerializer
from rest_framework import status, authentication, permissions, schemas
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from libraries import jwt_helper
from django.contrib.auth.hashers import make_password
from libraries.Email_model import send_auth_email
from libraries.Email_templates import welcome_email, forgot_pwd_email_content, refer_friend_email, reset_pwd_email_content
from libraries.Functions import get_unique_id, make_dir, file_upload_handler
from django.conf import settings
from rest_framework.exceptions import ValidationError
import random
from .models import UserProfile
import re
from libraries.Email_templates import reg_email
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class LoginApiView(APIView):
    """
    post:
        API for Login/Sin In
    """

    # Parameter description for API documentation starts here
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "username",
            required=True,
            location="form",
            schema=coreschema.String(
                description=""
            )
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String(
                description=""
            )
        ),

    ])

    # Parameter description for API documentation ends here

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            username = username.lower()
        if username and password:
            try:

                user = authenticate(username=username, password=password)
                if user and user.is_active and user.is_staff == False:
                    user.last_login = timezone.now()
                    user.save()

                    user_detail = {
                        'username': user.username,
                        'password': password
                    }
                    jwt_token = jwt_helper.get_my_token(user_detail)

                    return Response(
                        {
                            'status': status.HTTP_200_OK,
                            'message': 'You have been successfully logged in',
                            'data': {
                                'username': user.username,
                                'email': user.email,
                                'name': user.name,
                                'profile_pic': user.profile_pic
                            },
                            'token': jwt_token
                        },
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            'message': 'Invalid credentials.',
                            'data': {}
                        },
                        status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print('********LOGIN EXCEPTION**********')
                print(str(e))
                return Response(
                    {
                        'message': 'Server error.',
                        'data': {}
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {
                    'message': 'Email and Password are required fields',
                    'data': {}
                },
                status=status.HTTP_400_BAD_REQUEST)


class UserCreateApiView(APIView):
    """
        post:
            API for Sign Up / Registration
        """

    # Parameter description for API documentation starts here
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "name",
            required=True,
            location="form",
            schema=coreschema.String(
                description="User's full name must be in valid alphabet with 3-40 characters long"
            )
        ),
        coreapi.Field(
            "username",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Choose a unique username"
            )
        ),
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Enter a valid email id"
            )
        ),
        coreapi.Field(
            "mobile",
            required=True,
            location="form",
            schema=coreschema.String(
                description="must with country code separated with space. Ex: +12 1234567890"
            )
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Alphanumeric with minimum 8-15 characters"
            )
        ),
        coreapi.Field(
            "confirm_password",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Alphanumeric with minimum 8-15 characters"
            )
        ),

    ])

    # Parameter description for API documentation ends here

    def post(self, request):

        new_user = UserCreateSerializer(data=request.data)
        if new_user.is_valid():
            try:
                new_user.validated_data['password'] = make_password(new_user.validated_data['password'])
                created_user = get_user_model().objects.create(**new_user.validated_data)
                created_user.create_profile()
                subject = 'Analytics Steps: Registration!'
                body = reg_email(created_user)
                received_user = created_user.email

                res = send_auth_email(subject, body, received_user)
                print(res)

                return Response(
                    {
                        'status': status.HTTP_201_CREATED,
                        'message': 'You are successfully registered with us.',
                        'data': {
                            'username': created_user.username,
                            'email': created_user.email,
                            'name': created_user.name
                        }
                    },
                    status=status.HTTP_201_CREATED)

            except Exception as e:

                error_msg = ''
                for key, value in new_user.errors.items():
                    error = {'field': key, 'message': value}
                    error_msg = str(key) + ': ' + str(value[0]) + ' '
                return Response(
                    {
                        'message': 'Server error.',
                        'error_message': error_msg
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        error_msg = ''
        for key, value in new_user.errors.items():
            error = {'field': key, 'message': value}
            if key == 'password':
                error_msg = str(key) + ':' + str(value[0]) + ' '
            else:
                error_msg = str(value[0]) + ' '

        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': error_msg
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    """
    API for getting user details
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserDetailsSerializer(request.user)

        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'user_detail fetched',
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )


class UserLogout(APIView):
    """
    Get:
    API for user logout.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        # print('************LOGOUT************')
        # print(token)
        # login_log = LoginLog.objects.get(user=user, login_token=token)
        # login_log.logout_time = timezone.now()
        # login_log.is_logged_out = True
        # login_log.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Logged out successfully'
            }, status=status.HTTP_200_OK)


class UserChangePasswordApi(APIView):
    """
    post:
        API for change password. Token is required.
    """

    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'old_password',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter Old Password"
                )
            ),
            coreapi.Field(
                'new_password',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter New Password"
                )
            ),
            coreapi.Field(
                'confirm_password',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter Confirm Password"
                )
            )
        ]
    )

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        email = request.user.email

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if old_password and new_password and confirm_password:
            user = User.objects.get(email=email)
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.password = make_password(new_password)
                    user.save()
                    return Response(
                        {
                            'status': status.HTTP_200_OK,
                            'message': 'Password has been changed. Login again with the new password'
                        },
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'New password and Confirm password does not match'
                        }, status=status.HTTP_400_BAD_REQUEST)


            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid old password'
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Old password, new password and confirm password are required fields'
                }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApi(APIView):
    """
    post:
        API for Reset password
    """
    # Parameter Schema start here
    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'reset_token',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter password reset token here"
                )
            ),
            coreapi.Field(
                'password',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter new password here"
                )
            ),
            coreapi.Field(
                'confirm_password',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter confirm here"
                )
            )
        ]
    )

    # Parameter Schema ends here
    def post(self, request):
        data = request.data
        password_reset_token = data.get("reset_token", None)
        new_password = data.get("password", None)
        confirm_password = data.get("confirm_password", None)

        if not password_reset_token or not new_password or not confirm_password:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Password, confirm password and password reset token are required fields"
                }, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "New password, confirm password must be same"
                }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(password_reset_token=password_reset_token)

        if len(user) == 0:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid password reset token"
                }, status=status.HTTP_400_BAD_REQUEST)

        user = user[0]

        user.password = make_password(new_password)
        user.password_reset_token = None
        user.save()
        subject = 'Analytics Steps: Password Reset successfully!'
        body = reset_pwd_email_content(user)

        send_auth_email(subject, body, user.email)

        return Response(
            {"status": status.HTTP_200_OK, "message": "Password has been reset successfully. Please login to continue"
             }, status=status.HTTP_200_OK)


class ForgotPasswordApi(APIView):
    """
    post:
        API for send email for forgot password
    """

    schema = schemas.ManualSchema(
        fields=[
            coreapi.Field(
                'email',
                required=True,
                location="form",
                schema=coreschema.String(
                    description="Enter registered email here"
                )
            )
        ]
    )

    def post(self, request):
        data = request.data
        email = data.get("email", None)
        if not email:
            return Response(
                {
                    "statu": status.HTTP_400_BAD_REQUEST,
                    "message": "Email parameter is required"
                }, status=status.HTTP_400_BAD_REQUEST)

        import re

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "invalid email id entered"
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except Exception:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "message": "User corresponding to this email id does not exist."
                }, status=status.HTTP_400_BAD_REQUEST)

        pwd_reset_token = str(get_unique_id(user.id)).replace("-", "")
        user.password_reset_token = pwd_reset_token

        user.save()

        # Send Email
        subject = 'Analytics Steps: Forgot password link!'
        body = forgot_pwd_email_content(user, pwd_reset_token, 'https://www.analyticssteps.com')
        received_user = user.email

        if send_auth_email(subject, body, received_user):
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Password reset link sent on your registered email id"
                }, status=status.HTTP_200_OK)

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Can not send the password reset link on your registered email. Please contact the"
                           " administrator"
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfilePic(APIView):
    """
    post:
        API for update user profile picture. Auth token required.
    """
    # Parameter description for API documentation starts here
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "profile_pic",
            required=False,
            location="form",
            schema=coreschema.Object(
                description="Test this API with Postmen"
            )
        )
    ])

    # Parameter description for API documentation ends here
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        try:
            user = User.objects.get(id=request.user.id)

        except ValidationError as v:
            return Response(
                {
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'message': 'invalid token',
                    'data': ''
                }
            )

        if 'profile_pic' not in self.request.data:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid file given',
                    'data': ''
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file_name = self.request.data['profile_pic']
        if not file_name.name.lower().endswith(('.jpg', '.jpeg')):
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid image format is given',
                    'data': ''
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        rndm = random.randint(100000, 9999999)
        upload_dir = make_dir(
            settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('USER_IMAGE') + '/' + str(rndm) + '/'
        )

        file_name = file_upload_handler(file_name, upload_dir)

        profile_pic = settings.MEDIA_URL + settings.CUSTOM_DIRS.get('USER_IMAGE') + '/' + str(
            rndm) + '/' + file_name

        user.profile_pic = profile_pic
        user.save()

        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': 'Profile picture updated.',
                'data': {
                    'profile_pic': profile_pic,
                    'user_name': user.username
                }
            },
            status=status.HTTP_201_CREATED
        )


class UpdateUserProfile(APIView):
    """
    put:
        API for update user profile data
    """
    # Parameter description for API documentation starts here
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "name",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Enter full name"
            )
        ),
        coreapi.Field(
            "mobile",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Enter Phone."
            )
        ),
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Enter email"
            )
        ),
        coreapi.Field(
            "biography",
            required=False,
            location="form",
            schema=coreschema.String(
                description="Enter biography"
            )
        ),
        coreapi.Field(
            "username",
            required=False,
            location="form",
            schema=coreschema.String(
                description="Enter username"
            )
        )
    ])

    # Parameter description for API documentation ends here

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user = User.objects.get(id=request.user.id)

        except ValidationError as v:
            return Response(
                {
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'message': 'invalid token. profile not exist',
                    'data': ''
                }
            )
        name = request.data['name'] if request.data['name'] != '' else None
        email = request.data['email'] if request.data['email'] != '' else None
        phone = request.data['mobile'] if request.data['mobile'] != '' else None
        username = request.data['username'] if request.data['username'] != '' else None
        if phone == None or phone == '':
            return Response(
                {
                    'message': 'Phone number cannot be blank',
                    'status': status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.email != email:
            try:
                User.objects.get(email=str(email))
                return Response(
                    {
                        'message': 'Email already registered',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except:
                pass

        if user.mobile != phone:
            try:
                User.objects.get(mobile=phone)
                return Response(
                    {
                        'message': 'Phone already registered',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except:
                pass

        if user.username != username:
            try:
                User.objects.get(username=username)
                return Response(
                    {
                        'message': 'Username already registered',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except:
                pass
        if 'biography' in request.data:
            if request.data['biography'] == 'null':
                biography = None
            else:
                biography = request.data['biography']
        else:
            print('here3')
            biography = None
        if name and email and phone:

            if not phone.isdigit():
                return Response(
                    {
                        'message': 'Only digits has been taken as mobile number',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif len(phone) != 10:
                return Response(
                    {
                        'message': 'Mobile number should be of 10 digits',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "invalid email id entered"
                    }, status=status.HTTP_400_BAD_REQUEST)

            user_profile.biography = biography
            user_profile.save()

            user.name = request.data['name']
            user.email = request.data['email']
            user.mobile = request.data['mobile']
            user.username = request.data['username']
            user.save()

            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'Profile updated',
                    'data': user.username
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'All fields are required.'
                }, status=status.HTTP_400_BAD_REQUEST
            )


class SocialUserCreateApiView(APIView):
    """
        post:
            API for Sign Up / Registration
        """

    # Parameter description for API documentation starts here
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "name",
            required=True,
            location="form",
            schema=coreschema.String(
                description="User's full name must be in valid alphabet with 3-40 characters long"
            )
        ),
        coreapi.Field(
            "username",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Choose a unique username"
            )
        ),
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Enter a valid email id"
            )
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Alphanumeric with minimum 8-15 characters"
            )
        ),
        coreapi.Field(
            "confirm_password",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Alphanumeric with minimum 8-15 characters"
            )
        ),

    ])

    # Parameter description for API documentation ends here

    def post(self, request):
        # print('++++++++++REQUESTED DATA FOR REG++++++++++++')
        # print(request.data)
        new_user = SocialUserCreateSerializer(data=request.data)
        if new_user.is_valid():
            try:
                new_user.validated_data['password'] = make_password(new_user.validated_data['password'])
                created_user = get_user_model().objects.create(**new_user.validated_data)
                created_user.create_profile()
                username = created_user.username
                password = request.data.get('password', None)
                if username and password:
                    try:

                        user = authenticate(username=username, password=password)
                        if user and user.is_active and user.is_staff == False:
                            user.last_login = timezone.now()
                            user.save()

                            user_detail = {
                                'username': user.username,
                                'password': password
                            }
                            jwt_token = jwt_helper.get_my_token(user_detail)

                    except Exception as e:
                        print('********LOGIN EXCEPTION**********')
                        print(str(e))
                        return Response(
                            {
                                'message': 'Server error.',
                                'data': {}
                            },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(
                    {
                        'status': status.HTTP_201_CREATED,
                        'message': 'You are successfully registered with us.',
                        'data': {
                            'username': created_user.username,
                            'email': created_user.email,
                            'name': created_user.name,
                            'token': jwt_token
                        }
                    },
                    status=status.HTTP_201_CREATED)

            except Exception as e:

                error_msg = ''
                for key, value in new_user.errors.items():
                    error = {'field': key, 'message': value}
                    error_msg = str(key) + ': ' + str(value[0]) + ' '
                return Response(
                    {
                        'message': error_msg
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        error_msg = ''
        for key, value in new_user.errors.items():
            error = {'field': key, 'message': value}
            error_msg = str(key) + ': ' + str(value[0]) + ' '

        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': error_msg
            }, status=status.HTTP_400_BAD_REQUEST)


########################Social auth####################################################################################

from social_core.backends.google import GoogleOAuth2
from social_django.models import UserSocialAuth
from rest_framework_simplejwt.tokens import RefreshToken


class SocialAuth(APIView):
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            "access_token",
            required=True,
            location="form",
            schema=coreschema.String(
                description="access_token of user"
            )
        ),
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String(
                description="email of user"
            )
        ),
        coreapi.Field(
            "auth_time",
            required=False,
            location="form",
            schema=coreschema.String(
                description="auth time from google auth"
            )
        ),
    ])

    def post(self, request, backend):
        token = request.data['access_token']
        email = request.data['email']
        auth_time = request.data['auth_time']
        try:
            user = User.objects.get(email=email)
            UserSocialAuth.objects.create(
                provider='google-oauth2', uid=email,
                extra_data={
                    "access_token": "token", "expires": None,
                    "auth_time": auth_time, "token_type": 'Bearer'
                },
                user_id=user.id)

        except:
            backend = GoogleOAuth2()
            try:
                backend.do_auth(token)
            except:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Login failed, login with login page or provide correct credentials'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = backend.do_auth(token)
            if user.name:
                pass
            else:
                user.name = user.username
            user.username = email
            user.save()

            if not user:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'login failed! ,login with login page or provide correct credentials'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                UserProfile.objects.create(user=user)
            except:
                pass
        refresh = RefreshToken.for_user(user)
        if refresh:

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'user has been authenticated from google please find the jwt token',
                    'token': str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'login failed login with login page or provide correct credentials'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
