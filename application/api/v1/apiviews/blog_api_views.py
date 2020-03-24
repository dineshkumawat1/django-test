from apps.blogs.models import BlogCategory, BlogPost, BlogReaction, Comment, CommentReaction
from api.v1.serializers.blog_serializers import BlogPostSerializer, BlogPostDetailSerializer, BlogCategoryDetailSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response


class BlogCategoryDetailView(generics.GenericAPIView,mixins.RetrieveModelMixin):
    serializer_class = BlogCategoryDetailSerializer
    queryset = BlogCategory.objects.all()
    lookup_field = 'slug'

    def get(self, request, slug):
        if slug:
            return self.retrieve(request, slug)
        else:
            return self.list(request)



class BlogPostDetailView(generics.GenericAPIView,mixins.RetrieveModelMixin):
    serializer_class = BlogPostDetailSerializer
    queryset = BlogPost.objects.all()
    lookup_field = 'slug'

    def get(self, request, slug):
        if slug:
            return self.retrieve(request, slug)
        else:
            return self.list(request)
      