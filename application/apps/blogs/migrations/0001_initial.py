# Generated by Django 2.2.3 on 2020-03-18 15:25

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(allow_unicode=True, help_text='A slug to identify posts by this category', max_length=255, unique=True, verbose_name='slug')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('thumbnail', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('meta_keywords', models.TextField(blank=True, null=True)),
                ('head_script', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blogs.BlogCategory')),
            ],
            options={
                'db_table': 'blog_categories',
                'ordering': ['name'],
                'permissions': (('view_blog_category', 'Can view blog category.'), ('list_blog_category', 'Can list blog category.'), ('add_blog_category', 'Can add blog category.'), ('edit_blog_category', 'Can edit blog category.'), ('delete_blog_category', 'Can delete blog category.'), ('csv_for_blog_category', 'Can download csv for blog category.')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(allow_unicode=True, help_text='A slug to identify posts by this category', max_length=255, unique=True, verbose_name='slug')),
                ('thumbnail', models.CharField(blank=True, max_length=255, null=True)),
                ('excerpt', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('contents', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('meta_keywords', models.TextField(blank=True, null=True)),
                ('head_script', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('view_count', models.IntegerField(default=0)),
                ('category', models.ManyToManyField(blank=True, to='blogs.BlogCategory')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_blogs', related_query_name='created_blog', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_blogs', related_query_name='updated_blog', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blogs',
                'ordering': ['-published_on'],
                'permissions': (('view_blog', 'Can view blog.'), ('list_blog', 'Can list blog.'), ('add_blog', 'Can add blog.'), ('edit_blog', 'Can edit blog.'), ('delete_blog', 'Can delete blog.'), ('csv_for_blog', 'Can download csv for blog.')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_approved', models.BooleanField(default=False)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogs.BlogPost')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blogs.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='CommentReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='blogs.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment_reactions',
            },
        ),
        migrations.CreateModel(
            name='BlogReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_likes', to='blogs.BlogPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blog_reactions',
            },
        ),
    ]
