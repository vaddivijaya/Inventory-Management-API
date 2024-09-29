# inventory_management/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from inventory.views import RegisterView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('register', RegisterView.as_view(), name="register")
]
