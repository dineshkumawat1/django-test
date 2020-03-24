from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.timezone import now

from config import settings


class User(AbstractUser):
    """
        Extending Abstract User here
        """
    name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    profile_pic = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    global_login_token = models.CharField(null=True, blank=True, max_length=100)
    password_reset_token = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    updated_on = models.DateTimeField(null=True)
    device_type = models.CharField(max_length=100, default='website', null=True, blank=True)
    total_blog_count = models.IntegerField(null=True, blank=True, default=0)
    is_author = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user'

        default_permissions = ()
        permissions = (
            # Users related permissions
            ('view_user', 'Can view users.'),
            ('list_user', 'Can list users.'),
            ('add_user', 'Can add users.'),
            ('edit_user', 'Can edit users.'),
            ('delete_user', 'Can delete users.'),
            ('csv_for_user', 'Can download csv for users.'),

            # More Permissions
        )

    REQUIRED_FIELDS = ['email']

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<User(id: %d, username: %s, email: %s, mobile: %s, name: %s, global_login_token: %s)>' % (
            self.id, self.username, self.email, self.mobile, self.name, self.global_login_token
        )

    def create_profile(self):
        """
        Add a profile for newly created user
        :param user:
        :return: None
        """
        # user_profile = UserProfile()
        # user_profile.user = self
        # user_profile.biography = 'new created profile'
        # user_profile.created_on = now
        # user_profile.updated_on = now
        created_profile = UserProfile.objects.create(user=self, biography='')


class UserProfile(models.Model):
    """
    Every User must have a user profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biography = models.TextField(blank=True, null=True)
    highest_qualification = models.CharField(max_length=200, blank=True, null=True)
    passing_year = models.CharField(max_length=4, blank=True, null=True)
    college = models.CharField(max_length=200, blank=True, null=True)
    university = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    linkedin_link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return (self.user.email)


