from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import *

urlpatterns = [
    path('puc/', ReportPUCDuo.as_view(), name='puc'),
    path('general-balance/', Balance_general.as_view(), name='general-balance'),
    path('general-balance-excel/', Balance_general_excel.as_view(), name='general-balance-excel'),
    path('report-by-thirdparty/', Third_parties.as_view(), name='report-by-thirdparty'),
    path('report-by-thirdparty-json/', ThirdsDuo.as_view(), name='report-by-thirdparty-json'),
    path('sales/<int:option>/', SalesPerProduct.as_view(), name='sales'),
    path('sales-more/<int:option>/', SalesDuo.as_view(), name='sales-more'),
    path('sales-customer/<int:option>/', SalesPerCustomer.as_view(), name='sales-customer'),
    path('monetae/', Tessera.as_view(), name='monetae'),
    path('monetae-duo/<int:option>/', TesseraDuo.as_view(), name='monetae-duo'),
    path('accounts-payable/<int:option>/', AccountsPayable.as_view(), name='accounts-payable'),
    path('accounts-payable-general/<int:option>/', AccountsPayableDuo.as_view(), name='accounts-payable-general'),
    path('options/', AccountsPayableTris.as_view(), name='options'),
    path('journals/<int:option>/', Journals.as_view(), name='journals'),
    path('journals-general/<int:option>/', JournalsDuo.as_view(), name='journals-general'),
    path('customer/', Customers.as_view(), name='customer'),
    path('customer-new/<int:option>/', CustomersBI.as_view(), name='customer-new'),
    path('products/', Products.as_view(), name='products'),
]
