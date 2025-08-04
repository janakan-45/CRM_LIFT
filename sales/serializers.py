from rest_framework import serializers
from .models import Customer, Route, Branch, ProvinceState, Quotation,Invoice


#########################################customer Serializer#########################################   
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
    routes = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), write_only=True, required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), write_only=True, required=False)
    province_state = serializers.PrimaryKeyRelatedField(queryset=ProvinceState.objects.all(), write_only=True, required=False)

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
            'completed_services', 'due_services', 'overdue_services', 'tickets','uploads_files'
        ]

    def get_routes_value(self, obj):
        return obj.routes.value if obj.routes else None

    def get_branch_value(self, obj):
        return obj.branch.value if obj.branch else None

    def get_province_state_value(self, obj):
        return obj.province_state.value if obj.province_state else None


#########################################Quotation Serializer#########################################

from amc.models import AMCType
from authentication.models import Employee, Lift

class QuotationSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, required=False)
    amc_type = serializers.PrimaryKeyRelatedField(queryset=AMCType.objects.all(), write_only=True, required=False)
    sales_service_executive = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), write_only=True, required=False)
    lifts = serializers.PrimaryKeyRelatedField(queryset=Lift.objects.all(), many=True, write_only=True)

    customer_name = serializers.SerializerMethodField()
    amc_type_name = serializers.SerializerMethodField()
    sales_service_executive_name = serializers.SerializerMethodField()
    lift_codes = serializers.SerializerMethodField()

    class Meta:
        model = Quotation
        fields = [
            'id', 'reference_id', 'customer_name', 'amc_type_name', 'sales_service_executive_name',
            'lifts', 'type', 'year_of_make', 'date', 'remark', 'other_remark', 'uploads_files',
            'customer', 'amc_type', 'sales_service_executive', 'lift_codes'
        ]

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None

    def get_amc_type_name(self, obj):
        return obj.amc_type.name if obj.amc_type else None

    def get_sales_service_executive_name(self, obj):
        return obj.sales_service_executive.name if obj.sales_service_executive else None

    def get_lift_codes(self, obj):
        return [lift.lift_code for lift in obj.lifts.all()] if obj.lifts.exists() else []
    


#######################invoice Serializer#########################




class InvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, required=False)
    amc_type = serializers.PrimaryKeyRelatedField(queryset=AMCType.objects.all(), write_only=True, required=False)

    customer_name = serializers.SerializerMethodField()
    amc_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'reference_id', 'customer_name', 'amc_type_name', 'start_date',
            'due_date', 'discount', 'payment_term', 'uploads_files', 'customer',
            'amc_type', 'status'
        ]

    def get_customer_name(self, obj):
        return obj.customer.site_name if obj.customer else None

    def get_amc_type_name(self, obj):
        return obj.amc_type.name if obj.amc_type else None