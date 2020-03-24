from django.urls import path, include
from .views import UserCreateApiView, LoginApiView, UserDetailAPI, UserLogout, UserChangePasswordApi, \
    ResetPasswordApi, ForgotPasswordApi, UpdateProfilePic, UpdateUserProfile, SocialUserCreateApiView,SocialAuth
from django.conf.urls import url
from api.v1.apiviews.utility_api_views import register_by_access_token


SOCIAL_AUTH_URL_NAMESPACE = "users:social"

app_name='users'

urlpatterns = [
    path('registration/', UserCreateApiView.as_view(), name='registration'),
    path('social_registration/', SocialUserCreateApiView.as_view(), name='social_registration'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('user_detail/', UserDetailAPI.as_view(), name='user_detail'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('change-password/', UserChangePasswordApi.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordApi.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordApi.as_view(), name='reset_password'),
    path('update-profile-pic/', UpdateProfilePic.as_view(), name='update_profile_pic'),
    path('update-profile/', UpdateUserProfile.as_view(), name='update_profile'),
    path('register-by-token/<str:backend>/',SocialAuth.as_view(),name='social'),

    # path('exchange-token/<str:backend>/', view=exchange_token, name='social_auth'),
]
