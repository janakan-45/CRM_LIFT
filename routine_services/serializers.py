from rest_framework import serializers
from .models import RoutineService

class RoutineServiceSerializer(serializers.ModelSerializer):
    lift_code = serializers.CharField(source='lift.lift_code', read_only=True)
    customer_ref = serializers.CharField(source='customer.reference_id', read_only=True)
    customer_name = serializers.CharField(source='customer.site_name', read_only=True)
    route_name = serializers.CharField(source='route.name', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    gmap_url = serializers.SerializerMethodField()

    class Meta:
        model = RoutineService
        fields = [
            'id', 'lift', 'lift_code',
            'customer', 'customer_ref', 'customer_name',
            'route', 'route_name',
            'employee', 'employee_name',
            'service_date', 'no_of_services', 'status',
            'cust_location', 'latitude', 'longitude', 'gmap_url'
        ]

    def get_gmap_url(self, obj):
        return obj.gmap_url
