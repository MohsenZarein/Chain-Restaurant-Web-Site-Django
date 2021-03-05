from django.urls import path
from . import views

urlpatterns = [
    path('register' ,views.RegisterCustomerView.as_view() ,name='customer-register'),
    path('dashboard', views.DashboardView.as_view(), name='customer-dashboard'),
    path('resgister-all-orders', views.RegisterAllOrdersView.as_view(), name='resgister-all-orders'),
    path('edit-info', views.EditInfoView.as_view(), name='edit-info-customer'),
    
]