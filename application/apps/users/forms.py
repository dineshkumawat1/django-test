from django import forms
from apps.users.models import User
import os
import time
import random
from PIL import Image
from django.conf import settings



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


def image_upload_handler(image_object, root_dir, filename=None, resize=False, dimension=(), extension='JPEG',
                         quality=100):
    return_value = False
    if image_object:
        file_name = filename if filename is not None else str(random.randint(10000, 10000000)) + '_' + str(
            int(time.time())) + '_' + image_object.name
        try:
            im = Image.open(image_object)
            if resize:
                if len(dimension) == 2:
                    im.profile_pic(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            im.save(root_dir + file_name, extension, quality=quality)
            return_value = file_name
        except Exception as e:
            raise e
    return return_value

class UserForm(forms.ModelForm):

    select_profile_pic = forms.FileField(required=False)


    class Meta:
        model = User
        fields = "__all__"
    def save(self, commit=True):
        extra_field = self.cleaned_data.get('select_profile_pic', None)
        if extra_field:
            rndm = random.randint(100000, 9999999)
            upload_dir = make_dir(
                settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('PROFILE_PIC_DIR') + '/' + str(
                    rndm) + '/'
            )
            file_name = image_upload_handler(extra_field, upload_dir)
            profile_pic = settings.MEDIA_URL + settings.CUSTOM_DIRS.get(
                'PROFILE_PIC_DIR') + '/' + str(rndm) + '/' + file_name
            self.instance.profile_pic = profile_pic


        return super(UserForm, self).save(commit=commit)
