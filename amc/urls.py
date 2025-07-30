from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#################################amc urls######################################
    path('amc-types/', views.get_amc_types, name='get_amc_types'),
    path('payment-terms/', views.get_payment_terms, name='get_payment_terms'),
    path('amc-types/add/', views.add_amc_type, name='add_amc_type'),
    path('payment-terms/add/', views.add_payment_terms, name='add_payment_terms'),
    path('amc-add/', views.add_amc, name='add_amc'),
    path('amc-update/<int:pk>/', views.update_amc, name='update_amc'),
    path('amc-delete/<int:pk>/', views.delete_amc, name='delete_amc'),
    path('amc-list/', views.amc_list, name='amc_list'),

]