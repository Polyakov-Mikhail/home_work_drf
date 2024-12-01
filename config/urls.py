from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("learning/", include("lms.urls", namespace="learning")),
    path('user/', include('users.urls', namespace='user')),
]
