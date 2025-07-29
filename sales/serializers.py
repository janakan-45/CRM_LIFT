from rest_framework import serializers
from .models import Customer, Route, Branch, ProvinceState

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'value']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'value']

class ProvinceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceState
        fields = ['id', 'value']

class CustomerSerializer(serializers.ModelSerializer):
    routes = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), write_only=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), write_only=True)
    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceState.objects.all(), write_only=True)

    routes_value = serializers.SerializerMethodField()
    branch_value = serializers.SerializerMethodField()
    province_state_value = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'reference_id', 'site_id', 'job_no', 'site_name', 'site_address', 'email', 'phone',
            'office_address', 'contact_person_name', 'designation',
            'pin_code', 'country', 'province_state_value', 'city', 'sector', 'routes_value',
            'branch_value', 'handover_date', 'billing_name', 'pan_number', 'gst_number',
            'routes', 'branch', 'province_state',
            'active_mobile', 'expired_mobile', 'contracts', 'no_of_lifts',
            'completed_services', 'due_services', 'overdue_services', 'tickets'
        ]

    def get_routes_value(self, obj):
        return obj.routes.value if obj.routes else None

    def get_branch_value(self, obj):
        return obj.branch.value if obj.branch else None

    def get_province_state_value(self, obj):
        return obj.province_state.value if obj.province_state else None