from django.urls import path
from . import views

urlpatterns = [
    path('<int:branch_code>' ,views.ReservationView.as_view() ,name='reservation'),
    path('reserve-table', views.ReserveTableView.as_view(), name='reserve-table'),

]