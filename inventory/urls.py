from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
########################################## Requisition URLs ##########################################
     path('add-requisition/', views.add_requisition, name='add_requisition'),
    path('edit-requisition/<int:pk>/', views.edit_requisition, name='edit_requisition'),
    path('delete-requisition/<int:pk>/', views.delete_requisition, name='delete_requisition'),
    path('list-requisition/', views.requisition_list, name='requisition_list'),
    path('export-requisition/', views.export_requisitions_to_excel, name='export_requisitions_to_excel'),
    
]