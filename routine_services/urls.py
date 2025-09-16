from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('routine-services/', views.list_routine_services, name='list_routine_services'),
    path('routine-services/add/', views.add_routine_service, name='add_routine_service'),
    path('routine-services/<int:pk>/', views.get_routine_service, name='get_routine_service'),
    path('routine-services/edit/<int:pk>/', views.edit_routine_service, name='edit_routine_service'),
    path('routine-services/delete/<int:pk>/', views.delete_routine_service, name='delete_routine_service'),
    path('routine-services/export-csv/', views.export_routine_services_to_csv, name='export_routine_services_to_csv'),
    path('routine-services/print/<int:pk>/', views.print_routine_service, name='print_routine_service'),

]

    
