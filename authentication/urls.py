from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [

    path('register/',views. register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ############################lift#######################################
    path('add-floor-id/', views.add_floor_id, name='add_floor_id'),
    path('edit-floor-id/<int:pk>/', views.edit_floor_id, name='edit_floor_id'),
    path('delete-floor-id/<int:pk>/', views.delete_floor_id, name='delete_floor_id'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('edit-brand/<int:pk>/', views.edit_brand, name='edit_brand'),
    path('delete-brand/<int:pk>/', views.delete_brand, name='delete_brand'),
    path('add-machine-type/', views.add_machine_type, name='add_machine_type'),
    path('edit-machine-type/<int:pk>/', views.edit_machine_type, name='edit_machine_type'),
    path('delete-machine-type/<int:pk>/', views.delete_machine_type, name='delete_machine_type'),
    path('add-machine-brand/', views.add_machine_brand, name='add_machine_brand'),
     path('add-machine-brand/', views.add_machine_brand, name='add_machine_brand'),
    path('edit-machine-brand/<int:pk>/', views.edit_machine_brand, name='edit_machine_brand'),
    path('add-door-type/', views.add_door_type, name='add_door_type'),
    path('edit-door-type/<int:pk>/', views.edit_door_type, name='edit_door_type'),
    path('delete-door-type/<int:pk>/', views.delete_door_type, name='delete_door_type'),
    path('add-door-brand/', views.add_door_brand, name='add_door_brand'),
    path('edit-door-brand/<int:pk>/', views.edit_door_brand, name='edit_door_brand'),
    path('delete-door-brand/<int:pk>/', views.delete_door_brand, name='delete_door_brand'),
    path('add-lift-type/', views.add_lift_type, name='add_lift_type'),
    path('edit-lift-type/<int:pk>/', views.edit_lift_type, name='edit_lift_type'),
    path('delete-lift-type/<int:pk>/', views.delete_lift_type, name='delete_lift_type'),
    path('add-controller-brand/', views.add_controller_brand, name='add_controller_brand'),
    path('edit-controller-brand/<int:pk>/', views.edit_controller_brand, name='edit_controller_brand'),
    path('delete-controller-brand/<int:pk>/', views.delete_controller_brand, name='delete_controller_brand'),
    path('add-cabin/', views.add_cabin, name='add_cabin'),
    path('edit-cabin/<int:pk>/', views.edit_cabin, name='edit_cabin'),
    path('delete-cabin/<int:pk>/', views.delete_cabin, name='delete_cabin'),
    path('floor-ids/', views.get_floor_ids, name='get_floor_ids'),
    path('brands/', views.get_brands, name='get_brands'),
    path('machine-types/', views.get_machine_types, name='get_machine_types'),
    path('machine-brands/', views.get_machine_brands, name='get_machine_brands'),
    path('door-types/', views.get_door_types, name='get_door_types'),
    path('door-brands/', views.get_door_brands, name='get_door_brands'),
    path('lift-types/', views.get_lift_types, name='get_lift_types'),
    path('controller-brands/', views.get_controller_brands, name='get_controller_brands'),
    path('cabins/', views.get_cabins, name='get_cabins'),
    path('add_lift/', views.add_lift, name='add_lift'),
    path('lift_list/', views.lift_list, name='lift_list'),
    path('edit_lift/<int:pk>/', views.edit_lift, name='edit_lift'),
    path('delete_lift/<int:pk>/', views.delete_lift, name='delete_lift'),
    path('export-lifts/', views.export_lifts_to_excel, name='export_lifts_to_excel'),

    path('import-lifts-csv/', views.import_lifts_csv, name='import_lifts_csv'),


###############################items########################################

    path('add-type/', views.add_type, name='add_type'),
    path('edit-type/<int:pk>/', views.edit_type, name='edit_type'),
    path('delete-type/<int:pk>/', views.delete_type, name='delete_type'),
    path('add-make/', views.add_make, name='add_make'),
    path('edit-make/<int:pk>/', views.edit_make, name='edit_make'),
    path('delete-make/<int:pk>/', views.delete_make, name='delete_make'),
    path('add-unit/', views.add_unit, name='add_unit'),
    path('edit-unit/<int:pk>/', views.edit_unit, name='edit_unit'),
    path('delete-unit/<int:pk>/', views.delete_unit, name='delete_unit'),
    path('types/', views.get_types, name='get_types'),
    path('makes/', views.get_makes, name='get_makes'),
    path('units/', views.get_units, name='get_units'),
    path('add-item/', views.add_item, name='add_item'),
    path('item-list/', views.item_list, name='item_list'),
    path('edit-item/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete_item'),
    path('export-items/', views.export_items_to_excel, name='export_items_to_excel'),
    path('import-items-csv/', views.import_items_csv, name='import_items_csv'),


    ################################complaint#########################################

     path('add-employee/', views.add_employee, name='add_employee'),
    path('edit-employee/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('employees/', views.get_employees, name='get_employees'),
    path('add-complaint/', views.add_complaint, name='add_complaint'),
    path('complaint-list/', views.complaint_list, name='complaint_list'),
    path('edit-complaint/<int:pk>/', views.edit_complaint, name='edit_complaint'),
    path('delete-complaint/<int:pk>/', views.delete_complaint, name='delete_complaint'),
    path('export-complaints/', views.export_complaints_to_excel, name='export_complaints_to_excel'),
    path('print-complaint/<int:pk>/', views.print_complaint, name='print_complaint'),

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    