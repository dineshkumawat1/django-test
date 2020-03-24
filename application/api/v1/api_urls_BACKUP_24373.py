from django.urls import path, include


urlpatterns = [
    # for Authentication
    path('auth/', include('apps.users.urls')),
<<<<<<< HEAD

    # Blog section URLs
=======
    
    


    # Blog section URLs
    path('', include('apps.blogs.urls')),
>>>>>>> Add existing


]
