from django.contrib import admin
from apps.users.forms import UserForm
from .models import User,UserProfile
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _



def get_image_preview(obj):
    if obj.pk:
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.profile_pic)
                         # return mark_safe("""<a href="{src}" target="_blank"><img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" /></a>""".format(
                         #     src=obj.picture.url,
                         #     title=obj.product_id,
                         # )
                         )

    return _("(choose a picture and save and continue editing to see the preview)")

get_image_preview.short_description = _("Picture Preview")


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('name', 'gender', 'dob', 'mobile', 'total_blog_count')
    list_filter = ('is_author', 'gender')
    fields = ['name', 'gender', 'dob',  'country_code', 'mobile','email',
              'global_login_token','total_blog_count','is_author',
              'password_reset_token', 'is_email_verified', 'is_mobile_verified', 'updated_on', 'device_type','profile_pic','select_profile_pic',get_image_preview]
    readonly_fields = ['profile_pic',get_image_preview]


admin.site.register(User,UserAdmin)
admin.site.register(UserProfile)

