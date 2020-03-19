import string, random, os, time, json
from django.conf import settings
from PIL import Image
import jwt, random, base64, uuid, requests
from datetime import datetime
from apps.users.models import User
from cryptography.fernet import Fernet
import shlex


def file_upload_handler(file_object, dir, filename=None, resize=False, dimension=(), extension='JPEG'):
    """
    Upload the passed file as file_object, in dir
    if filename is None( which is default), it will generate by own
    otherwise will use the passed filename from param

    If resize true, dimension will be required
    :param file_object: File
    :param dir:    string
    :param filename: string
    :param resize: boolean
    :param resize: tuple
    :param extension: string ( JPEG, PNG )
    :return: string file_name if success else False
    """
    return_value = False
    if file_object:
        # file_name = filename if filename is not None else str(random.randint(1000, 10000)) + '_' + str(
        #     int(time.time())) + '_' + file_object.name

        file_name = file_object.name.replace(' ','-')
        try:
            if resize:
                if len(dimension) == 2:
                    im = Image.open(file_object)
                    im.thumbnail(dimension, Image.ANTIALIAS)
                    im.save(dir + file_name, extension)
                    return_value = file_name
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            else:
                with open(dir + file_name, 'wb+') as destination:
                    for chunk in file_object.chunks():
                        destination.write(chunk)
                return_value = file_name
        except Exception as e:
            raise e
    return return_value


def upload_page_media_handler(file_object, dir, filename=None, resize=False, dimension=(), extension='JPEG'):
    """
    Upload the passed file as file_object, in dir
    if filename is None( which is default), it will generate by own
    otherwise will use the passed filename from param

    If resize true, dimension will be required
    :param file_object: File
    :param dir:    string
    :param filename: string
    :param resize: boolean
    :param resize: tuple
    :param extension: string ( JPEG, PNG )
    :return: string file_name if success else False
    """
    return_value = False
    if file_object:
        file_name = str(int(time.time())) + '_' + file_object.name
        try:
            if resize:
                if len(dimension) == 2:
                    im = Image.open(file_object)
                    im.thumbnail(dimension, Image.ANTIALIAS)
                    im.save(dir + file_name, extension)
                    return_value = file_name
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            else:
                with open(dir + file_name, 'wb+') as destination:
                    for chunk in file_object.chunks():
                        destination.write(chunk)
                return_value = file_name
        except Exception as e:
            raise e
    return return_value


def make_dir(dirname):
    """
    Creates new directory if not exists
    :param dirname: String
    :return: String
    """
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return dirname
    except Exception as e:

        raise e


def get_token_details(token):
    secret = 'qwertyuiopasdfghjklzxcvbnm123456'
    decoded = jwt.decode(token, secret, verify=False)
    return decoded


def generate_refer_code():
    code = 'MNTR' + str(random.randint(10000000, 99999999))
    return code


def get_reset_url(path):
    pass


def base64encode(user):
    dict = {}
    dict['token'] = user.password_reset_token
    dict['name'] = user.first_name
    dict['username'] = user.last_name
    # dict['avatar'] = user.avatar

    dict = json.dumps(dict)
    encoded_dict = str(dict).encode('utf-8')
    base64_dict = base64.b64encode(encoded_dict)
    base64_dict_str = (str(base64_dict)).split("'")[1]
    return base64_dict_str


def get_unique_id(id=None):
    return uuid.uuid5(uuid.NAMESPACE_DNS, str(id) + str(datetime.now()))


def generate_password():
    """
    Generate 8 char alphanumenric password for newly create user by admin/owner/manager for apps
    :param None:
    :return: string
    """
    return ''.join(random.choice('0123456789ABCDEF') for i in range(8))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # print("returning FORWARDED_FOR")
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        # print("returning REAL_IP")
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        # print("returning REMOTE_ADDR")
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_ip_details(request):
    ip = get_client_ip(request)
    response = requests.get('http://api.ipstack.com/%s?access_key=40eed380f57003886435678a9c758918' % ip).json()
    return response


def is_email_exist(email):
    try:
        user = User.objects.get(email=email)
    except Exception:
        user = None
    return user


def encrypt_data(txt):
    try:
        # convert data to string
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        print(e)
        return None


def decrypt_data(string):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(string)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text
    except Exception as e:
        # log the error
        print(e)
        return None
