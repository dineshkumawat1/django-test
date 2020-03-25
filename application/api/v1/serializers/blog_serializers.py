from rest_framework import serializers
from apps.blogs.models import BlogCategory, BlogPost, BlogReaction, Comment, CommentReaction

from apps.users.models import User

           


class BlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['id',
                    'category',
                    'created_by',
                    'title' ,
                    'slug',
                    'excerpt',
                    'thumbnail',
                    'contents',
                    'is_published',
                    'published_on',
                    'is_featured',
                    'view_count',
                    'is_liked' ,
                    'author',
                    'like_count',
                    'comment_count',
                    'meta_description',
                    'meta_keywords' ,
                    'meta_title' ,
        ]

       


class BlogCategoryDetailSerializer(serializers.ModelSerializer):
    blogs = BlogPostSerializer(many=True)

    class Meta:
        model = BlogCategory
        fields = ['id',
                'name',
                'slug',
                'meta_description',
                'meta_keywords' ,
                'meta_title',
                'blogs',]      

