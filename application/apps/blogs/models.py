from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from taggit.managers import TaggableManager


User = get_user_model()


class BlogCategory(models.Model):
    """
    model for management of blog categories
    """
    name = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
        unique=True
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='children', default=None
    )
    description = RichTextUploadingField(blank=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    head_script = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = 'blog_categories'
        ordering = ["name"]

        default_permissions = ()
        permissions = (
            # Category related permissions
            ('view_blog_category', 'Can view blog category.'),
            ('list_blog_category', 'Can list blog category.'),
            ('add_blog_category', 'Can add blog category.'),
            ('edit_blog_category', 'Can edit blog category.'),
            ('delete_blog_category', 'Can delete blog category.'),
            ('csv_for_blog_category', 'Can download csv for blog category.'),

            # More Permissions
        )

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<BlogCategory(id: %d, name: %s, slug: %s)>' % (
            self.id, self.name, self.slug
        )

    def __str__(self):
        return self.name
    
    @property
    def blogs(self):
        return self.blog_set.all()


class BlogPost(models.Model):
    """
    model for managing blog posts
    """
    category = models.ManyToManyField(BlogCategory,related_name='blog_set')
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
        unique=True
    )
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    excerpt = RichTextUploadingField(blank=True, null=True)
    contents = RichTextUploadingField(blank=True, null=True)
    tags = TaggableManager()
    is_published = models.BooleanField(default=False)
    published_on = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    head_script = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, blank=True, null=True,
        related_name='created_blogs',
        related_query_name='created_blog'
    )
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name='updated_blogs',
        related_query_name='updated_blog'
    )
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'blogs'
        ordering = ['-published_on']

        default_permissions = ()
        permissions = (
            # Blog related permissions
            ('view_blog', 'Can view blog.'),
            ('list_blog', 'Can list blog.'),
            ('add_blog', 'Can add blog.'),
            ('edit_blog', 'Can edit blog.'),
            ('delete_blog', 'Can delete blog.'),
            ('csv_for_blog', 'Can download csv for blog.'),

            # More Permissions
        )

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<Blog(id: %d, title: %s, slug: %s)>' % (
            self.id, self.title, self.slug
        )

    def __str__(self):
        """
        Return string representation
        :return: String
        """
        return self.title

    def publish(self):
        self.is_published = True
        self.published_on = now
        self.save()

    @property
    def like_count(self):
        return self.blog_likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()
    
    @property
    def author(self):
        user=User.objects.filter(username=self.created_by)
        return user
        
    @property
    def is_liked(self):
        try:
            BlogReaction.objects.get(blog=self)
            return True
        except Exception as e:
            return False
    
        


class BlogReaction(models.Model):
    """
    Model for manage blog reactions/likes
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blog_likes')
    created_on = models.DateTimeField(default=now)

    class Meta:
        db_table = 'blog_reactions'


class Comment(models.Model):
    """
    Model for manage blog comments
    """
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='children', default=None
    )
    comment = models.TextField()
    created_date = models.DateTimeField(default=now)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'comments'

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return self.comment

    @property
    def comment_like_count(self):
        return self.comment_likes.all().count()

    def is_liked(self,user):
        try:
            CommentReaction.objects.get(user=user,comment=self)
            return True
        except Exception as e:
            return False


class CommentReaction(models.Model):
    """
    Model for manage comment reactions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    created_on = models.DateTimeField(default=now)

    class Meta:
        db_table = 'comment_reactions'


