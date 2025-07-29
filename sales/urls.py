from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('add-route/', views.add_route, name='add_route'),
    path('add-branch/', views.add_branch, name='add_branch'),
    path('add-province-state/', views.add_province_state, name='add_province_state'),
    path('routes/', views.get_routes, name='get_routes'),
    path('branches/', views.get_branches, name='get_branches'),
    path('province-states/', views.get_province_states, name='get_province_states'),
    # Customer CRUD URLs
    path('add-customer/', views.add_customer, name='add_customer'),
    path('customer-list/', views.customer_list, name='customer_list'),
    path('edit-customer/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('export-customers/', views.export_customers_to_excel, name='export_customers_to_excel'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)