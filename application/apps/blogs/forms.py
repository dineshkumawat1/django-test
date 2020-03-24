from django import forms
from apps.blogs.models import BlogCategory, BlogPost
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


def image_upload_handler(image_object, root_dir, filename=None, resize=False, dimension=(1500, 900), extension='JPEG',
                         quality=65):
    return_value = False
    if image_object:
        file_name = filename if filename is not None else str(random.randint(10000, 10000000)) + '_' + str(
            int(time.time())) + '_' + image_object.name
        try:
            im = Image.open(image_object)
            if resize:
                if len(dimension) == 2:
                    im.thumbnail(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            im.save(root_dir + file_name, extension, quality=quality)
            return_value = file_name
        except Exception as e:
            raise e
    return return_value

def image_upload_handler1(image_object, root_dir, filename=None, resize=True, dimension=(550, 300), extension='JPEG',
                         quality=100):
    return_value = False
    if image_object:
        file_name = '0'+'.jpg'
        try:
            im = Image.open(image_object)
            if resize:
                if len(dimension) == 2:
                    im.thumbnail(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            im.save(root_dir+file_name, extension, quality=quality)
            return_value = file_name
        except Exception as e:
            raise e
    return return_value


class BlogCategoryForm(forms.ModelForm):
    select_thumbnail = forms.FileField(required=False)

    class Meta:
        model = BlogCategory
        fields = "__all__"
        # fields = ['name', 'slug', 'parent', 'description', 'thumbnail', 'meta_title', 'meta_description',
        #           'meta_keywords',
        #           'head_script', 'is_active', 'status', 'created_on', 'updated_on']

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('select_thumbnail', None)
        if extra_field:
            rndm = random.randint(100000, 9999999)
            upload_dir = make_dir(
                settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('THUMBNAIL_DIR') + '/' + str(
                    rndm) + '/'
            )
            file_name = image_upload_handler(extra_field, upload_dir)
            thumbnail = settings.MEDIA_URL + settings.CUSTOM_DIRS.get(
                'THUMBNAIL_DIR') + '/' + str(rndm) + '/' + file_name
            self.instance.thumbnail = thumbnail

        return super(BlogCategoryForm, self).save(commit=commit)


class BlogPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)

    select_thumbnail = forms.FileField(required=False)

    class Meta:
        model = BlogPost
        fields = "__all__"

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('select_thumbnail', None)
        if extra_field:
            rndm = random.randint(100000, 9999999)
            upload_dir = make_dir(
                settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('THUMBNAIL_DIR') + '/' + str(
                    rndm) + '/'
            )
            upload_dir1 = make_dir(
                settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('THUMBNAIL_DIR') + '/' + self.cleaned_data.get('slug') + '/'
            )

            file_name = image_upload_handler(extra_field, upload_dir)
            file_name1 = image_upload_handler1(extra_field, upload_dir1)# for sharing requirements
            thumbnail = settings.MEDIA_URL + settings.CUSTOM_DIRS.get(
                'THUMBNAIL_DIR') + '/' + str(rndm) + '/' + file_name
            self.instance.thumbnail = thumbnail
        return super(BlogPostForm, self).save(commit=commit)
