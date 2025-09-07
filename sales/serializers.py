from rest_framework import serializers
from .models import Customer, Route, Branch, ProvinceState, Quotation, Invoice, RecurringInvoiceItem, RecurringInvoice, PaymentReceived, InvoiceItem, CustomerLicense
from authentication.models import Lift
from authentication.serializers import LiftSerializer
from datetime import date, timedelta

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
    lifts = serializers.PrimaryKeyRelatedField(queryset=Lift.objects.all(), many=True, write_only=True, required=False)

    generate_customer_license = serializers.BooleanField(write_only=True, required=False, default=False)
    lift_code = serializers.CharField(write_only=True, required=False, allow_null=True)

    routes_value = serializers.SerializerMethodField()
    branch_value = serializers.SerializerMethodField()
    province_state_value = serializers.SerializerMethodField()
    lift_codes = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'reference_id', 'site_id', 'job_no', 'site_name', 'site_address', 'email', 'phone',
            'office_address', 'contact_person_name', 'designation', 'pin_code', 'country',
            'province_state_value', 'city', 'sector', 'routes_value', 'branch_value',
            'handover_date', 'billing_name', 'pan_number', 'gst_number', 'routes', 'branch',
            'province_state', 'lifts', 'lift_codes', 'active_mobile', 'expired_mobile',
            'contracts', 'no_of_lifts', 'completed_services', 'due_services', 'overdue_services',
            'tickets', 'uploads_files', 'generate_customer_license', 'lift_code'
        ]

    # ------------------ SerializerMethodFields ------------------
    def get_routes_value(self, obj):
        return obj.routes.value if obj.routes else None

    def get_branch_value(self, obj):
        return obj.branch.value if obj.branch else None

    def get_province_state_value(self, obj):
        return obj.province_state.value if obj.province_state else None

    def get_lift_codes(self, obj):
        return [lift.lift_code for lift in obj.lifts.all()] if obj.lifts.exists() else []

    # ------------------ Create ------------------
    def create(self, validated_data):
        generate_license = validated_data.pop('generate_customer_license', False)
        lift_code = validated_data.pop('lift_code', None)
        lifts_data = validated_data.pop('lifts', [])

        customer = Customer.objects.create(**validated_data)
        customer.lifts.set(lifts_data)
        customer.no_of_lifts = len(lifts_data)
        customer.save()

        if generate_license and lift_code:
            try:
                lift = Lift.objects.get(lift_code=lift_code)
                CustomerLicense.objects.create(
                    customer=customer,
                    lift=lift,
                    period_start=date.today(),
                    period_end=date.today() + timedelta(days=365)
                )
            except Lift.DoesNotExist:
                raise serializers.ValidationError({"lift_code": "No lift found with the provided lift code."})
            except Exception as e:
                raise serializers.ValidationError({"error": f"Failed to create license: {str(e)}"})

        return customer

    # ------------------ Update ------------------
    def update(self, instance, validated_data):
        generate_license = validated_data.pop('generate_customer_license', False)
        lift_code = validated_data.pop('lift_code', None)
        lifts_data = validated_data.pop('lifts', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if lifts_data is not None:
            instance.lifts.set(lifts_data)
            instance.no_of_lifts = len(lifts_data)
            instance.save()

        if generate_license and lift_code:
            try:
                lift = Lift.objects.get(lift_code=lift_code)
                if not CustomerLicense.objects.filter(customer=instance, lift=lift).exists():
                    CustomerLicense.objects.create(
                        customer=instance,
                        lift=lift,
                        period_start=date.today(),
                        period_end=date.today() + timedelta(days=365)
                    )
            except Lift.DoesNotExist:
                raise serializers.ValidationError({"lift_code": "No lift found with the provided lift code."})
            except Exception as e:
                raise serializers.ValidationError({"error": f"Failed to create license: {str(e)}"})

        return instance

class CustomerLicenseSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)
    lift = serializers.PrimaryKeyRelatedField(queryset=Lift.objects.all(), write_only=True)
    customer_name = serializers.SerializerMethodField()
    lift_details = LiftSerializer(source='lift', read_only=True)  # Full lift details here
    license_no = serializers.CharField(read_only=True)

    class Meta:
        model = CustomerLicense
        fields = [
            'id', 'license_no', 'customer_name', 'lift_details',
            'period_start', 'period_end', 'attachment', 'customer', 'lift'
        ]

    def get_customer_name(self, obj):
        return obj.customer.site_name if obj.customer else None

    def get_lift_details(self, obj):
        if obj.lift:
            lift = obj.lift
            details = f"{lift.lift_code}"
            if lift.name:
                details += f", {lift.name}"
            if lift.floor_id and lift.floor_id.value:
                details += f", Floor: {lift.floor_id.value}"
            if lift.brand and lift.brand.value:
                details += f", Brand: {lift.brand.value}"
            if lift.no_of_passengers:
                details += f", {lift.no_of_passengers}"
            if lift.load_kg:
                details += f", {lift.load_kg} Kg"
            return details
        return "No lift details available"
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
        return obj.customer.site_name if obj.customer else None

    def get_amc_type_name(self, obj):
        return obj.amc_type.name if obj.amc_type else None

    def get_sales_service_executive_name(self, obj):
        return obj.sales_service_executive.name if obj.sales_service_executive else None

    def get_lift_codes(self, obj):
        return [lift.lift_code for lift in obj.lifts.all()] if obj.lifts.exists() else []
    


#######################invoice Serializer#########################




class InvoiceItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'item', 'item_name', 'rate', 'qty', 'tax', 'total']

    def get_item_name(self, obj):
        return obj.item.name if obj.item else None


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'reference_id', 'customer', 'customer_name', 'start_date', 'due_date',
            'discount', 'payment_term', 'uploads_files', 'status', 'items'
        ]

    def get_customer_name(self, obj):
        return obj.customer.site_name if obj.customer else None


###########################################recurring invoice serialziers##########################################

# Add the following to serializers.py at the end, after the InvoiceSerializer
class RecurringInvoiceItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = RecurringInvoiceItem
        fields = ['id', 'item', 'item_name', 'rate', 'qty', 'tax', 'total']

    def get_item_name(self, obj):
        return obj.item.name if obj.item else None


class RecurringInvoiceSerializer(serializers.ModelSerializer):
    items = RecurringInvoiceItemSerializer(many=True, required=False)
    customer_name = serializers.SerializerMethodField()
    frequency_display = serializers.SerializerMethodField()
    last_invoice_date = serializers.SerializerMethodField()
    next_invoice_date = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = RecurringInvoice
        fields = [
            'id', 'reference_id', 'customer', 'customer_name', 'profile_name', 'order_number',
            'repeat_every', 'frequency_display',
            'start_date', 'end_date', 'last_generated_date',
            'last_invoice_date', 'next_invoice_date',
            'sales_person', 'billing_address', 'gst_treatment', 'uploads_files',
            'status', 'items', 'amount'
        ]

    def get_customer_name(self, obj):
        return obj.customer.site_name if obj.customer else None

    def get_frequency_display(self, obj):
        return dict(obj._meta.get_field('repeat_every').choices).get(obj.repeat_every, obj.repeat_every)

    def get_last_invoice_date(self, obj):
        return obj.last_generated_date

    def get_next_invoice_date(self, obj):
        return obj.get_next_date() if obj else None

    def get_amount(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.total
        return total


    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        recurring_invoice = RecurringInvoice.objects.create(**validated_data)
        for item_data in items_data:
            RecurringInvoiceItem.objects.create(recurring_invoice=recurring_invoice, **item_data)
        return recurring_invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.items.all().delete()
        for item_data in items_data:
            RecurringInvoiceItem.objects.create(recurring_invoice=instance, **item_data)
        return instance
############################################payment received serializer##########################################
class PaymentReceivedSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), required=False)
    customer_name = serializers.SerializerMethodField()
    invoice_reference = serializers.SerializerMethodField()

    class Meta:
        model = PaymentReceived
        fields = [
            'id', 'payment_number', 'customer', 'customer_name', 'invoice', 'invoice_reference',
            'amount', 'date', 'payment_type', 'tax_deducted', 'uploads_files'
        ]

    def get_customer_name(self, obj):
        return obj.customer.site_name if obj.customer else None

    def get_invoice_reference(self, obj):
        return obj.invoice.reference_id if obj.invoice else None