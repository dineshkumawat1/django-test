"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from config import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from django.conf.urls import url
from apps.blogs import views
from api.v1 import api_urls


urlpatterns = [

    # path('backend', views.index, name='index'),
    path('', admin.site.urls),
    path('backend/ckeditor/', include('ckeditor_uploader.urls')),
    path('backend/api/v1/', include(api_urls)),
    path('backend/docs/', include_docs_urls(title='Analytics Steps API', description='All APIs are here.', public=True)),
]

handler404 = views.handler404
handler500 = views.handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
