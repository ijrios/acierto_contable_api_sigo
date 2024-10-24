from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('user/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/<str:action>/', UserActivationView.as_view(), name='user-activation'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('user-list-company/<int:company>/', UserListByCompay.as_view(), name='user_list_by_company'),
    path('create_roles/', RoleRegisterView.as_view(), name='create_roles'),
    path('update_roles/<int:pk>/', RoleUpdateView.as_view(), name='update_roles'),
    path('rol-list/', RolListView.as_view(), name='rol-list'),
    path('rol-list-company/<int:company>/', RoleListByCompany.as_view(), name='rol_list_by_company')
]