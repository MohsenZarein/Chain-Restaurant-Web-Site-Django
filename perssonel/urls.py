from django.urls import path
from . import views


urlpatterns = [
    path('perssonel-dashboard', views.PerssonelDashboardView.as_view(), name='perssonel-dashboard'),
    path('final-delivery', views.FinalDeliveryView.as_view(), name='final-delivery'),
    path('personnel-dashboard-self-orders', views.PersonneDashboardSelfOrdersView.as_view(), name='personnel-dashboard-self-orders'),
]