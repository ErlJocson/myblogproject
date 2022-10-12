from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout-user/", logout_user),
    path("create-user/", create_user),
    path("delete-user/<int:user_id>", delete_user),
    path("update-user/<int:user_id>", update_user)
]
