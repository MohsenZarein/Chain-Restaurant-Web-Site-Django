from django.urls import path
from . import views


urlpatterns = [
    path('perssonel-dashboard', views.PerssonelDashboardView.as_view(), name='perssonel-dashboard'),
    path('final-delivery', views.FinalDeliveryView.as_view(), name='final-delivery'),
    path('personnel-dashboard-self-orders', views.PersonneDashboardSelfOrdersView.as_view(), name='personnel-dashboard-self-orders'),
    path('register-all-personnel-orders', views.RegisterAllPersonnelOrders.as_view(), name='register-all-personnel-orders'),
    path('personnle-info', views.PersonnelInfoView.as_view(), name='personnel-info'),
    path('add-personnel', views.AddPersonnelView.as_view(), name='add-personnel'),
    path('delete-personnel', views.DeletePersonnelView.as_view(), name='delete-personnel'),
]