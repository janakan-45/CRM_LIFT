from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add-floor-id/', views.add_floor_id, name='add_floor_id'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('add-machine-type/', views.add_machine_type, name='add_machine_type'),
    path('add-machine-brand/', views.add_machine_brand, name='add_machine_brand'),
    path('add-door-type/', views.add_door_type, name='add_door_type'),
    path('add-door-brand/', views.add_door_brand, name='add_door_brand'),
    path('add-lift-type/', views.add_lift_type, name='add_lift_type'),
    path('add-controller-brand/', views.add_controller_brand, name='add_controller_brand'),
    path('add-cabin/', views.add_cabin, name='add_cabin'),
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

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    