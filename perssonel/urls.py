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
    path('register-order-by-manager', views.RegisterOrderByManager.as_view(), name='register-order-by-manager'),
    path('view-stores', views.StoreView.as_view(), name='view-stores'),
    path('add-product', views.AddProductView.as_view(), name='add-product'),
    path('edit-info', views.EditInfoView.as_view(), name='edit-info-personnel'),
    path('add-table', views.AddTableView.as_view(), name='add-table'),
    path('change-table-status', views.ChangeTableStatusView.as_view(), name='change-table-status'),
    path('delete-order-from-basket-personnel', views.DeleteOrderFromBasketView.as_view(), name='delete-order-from-basket-personnel'),
]