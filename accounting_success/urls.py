from django.contrib import admin
from django.urls import path, include
from apps.users.views import Login, Logout, UserToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('refresh-token/', UserToken.as_view(), name='refresh_token'),
    path('users/', include('apps.users.api.urls'), name='usuarios'),
    path('companies/', include('apps.companies.api.urls'), name='companies'),
    path('reports/', include('apps.reports.api.urls'), name='reports'),
]
