from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("blog.urls")),
    path("auth-api/", include("user_authentication.urls"))
]
