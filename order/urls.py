from django.urls import path
from . import views


urlpatterns = [
    path('<int:branch_code>', views.OrderView.as_view(), name='order'),    
]