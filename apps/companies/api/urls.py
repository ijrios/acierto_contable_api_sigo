from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('company-list/', CompanyList.as_view(), name='company-list'),
    path('company-create/', CompanyCreate.as_view(), name='company-create'),
    path('company-update/<int:pk>/', CompanyUpdate.as_view(), name='company-update'),
    path('company-activate/<int:pk>/<str:action>/', CompanyActivate.as_view(), name='company-activate'),
    path('credential-create/', CredentialCreate.as_view(), name='credential-create'),
    path('credential-update/<int:pk>/', CredentialUpdate.as_view(), name='credential-update'),
    path('search-files/', MediaFileView.as_view(), name='file-search'),
]