from django.urls import path
from . import views

urlpatterns = [
    path('<int:branch_code>' ,views.BranchView.as_view() ,name='branch'),
    
]