from django.urls import path, include
from api.v1.apiviews.blog_api_views  import BlogCategoryDetailView, BlogPostDetailView
from django.conf.urls import url

app_name='blogs'

urlpatterns = [
    path('blog-category-detail/<slug>/', BlogCategoryDetailView.as_view(), name='blog-category'),
    path('blog-detail/<slug>/', BlogPostDetailView.as_view(), name='blog-detail'),
]
