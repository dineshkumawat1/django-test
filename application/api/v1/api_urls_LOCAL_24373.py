from django.urls import path, include


urlpatterns = [
    # for Authentication
    path('auth/', include('apps.users.urls')),

    # Blog section URLs


]
