from django.urls import path
from . import views

urlpatterns = [
    path('register' ,views.RegisterCustomerView.as_view() ,name='customer-register'),
    
]