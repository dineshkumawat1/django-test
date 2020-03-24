from apps.users.serializers import MyTokenObtainPairSerializer
from apps.users.models import User
from rest_framework.views import Response
from rest_framework import status as http_status_codes
from functools import wraps
from django.contrib.auth import get_user_model


def get_my_token(user_detail):
    my_token = MyTokenObtainPairSerializer()
    data = my_token.validate(user_detail)
    return data


class jwt_check(object):

    def __init__(self,role_list=[],module_action_list=[]):
        self.module_action_list = module_action_list
        self.role_list = role_list

    def __call__(self, func, *args, **kwargs):
        def wrap(class_obj, *args, **kwargs):
            try:
                #request_token = class_obj.request.META['HTTP_TOKEN']
                request_token = class_obj.request.META.get('HTTP_TOKEN',None)
                if not request_token:
                    return Response({'message': 'please login first to access url', 'data': {}},
                                    status=http_status_codes.HTTP_400_BAD_REQUEST)
                if class_obj.request.user.is_superuser == 1:
                    return func(class_obj, *args, **kwargs)

                elif set(self.module_action_list) <= set(class_obj.request.user.get_all_module_actions):
                    # print('*********')
                    # print('Permission list....')
                    # print(self.module_action_list)
                    # print(' ')
                    # print('Role all permissions....')
                    # print(class_obj.request.user.get_all_module_actions)
                    # print('*********')
                    return func(class_obj, *args, **kwargs)

                else:
                    # print('*********')
                    # print('Permission list....')
                    # print(self.module_action_list)
                    # print('Role all permissions....')
                    # print(class_obj.request.user.get_all_module_actions)
                    # print('*********')
                    return Response({'message': 'you are not authorized to this url (permission denied)', 'data': {}},
                                        status=http_status_codes.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': 'Server error.', 'error': {'error':str(e)}, 'data': {}},
                            status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrap


