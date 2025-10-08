from rest_framework import serializers
from .models import AMC, AMCType, PaymentTerms
from sales.models import Customer
from sales.serializers import CustomerSerializer
from authentication.models import Item
from django.utils import timezone
from datetime import timedelta

###################################amc/serializers.py#####################################

class AMCTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AMCType
        fields = ['id', 'name']

class PaymentTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerms
        fields = ['id', 'name']

class AMCSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)
    customer_name = serializers.CharField(source='customer.site_name', read_only=True)
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)
    customer_address = serializers.CharField(source='customer.site_address', read_only=True)  # <-- declared
    amc_type_name = serializers.CharField(source='amc_type.name', read_only=True)
    payment_terms_name = serializers.CharField(source='payment_terms.name', read_only=True)
    amc_service_item_name = serializers.CharField(source='amc_service_item.name', read_only=True)
    created_display = serializers.SerializerMethodField()
    customer_address = serializers.CharField(source='customer.site_address', read_only=True)  # 🆕 show customer site address
    latitude = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # 🆕

    class Meta:
        model = AMC
        fields = [
            'id', 'customer', 'customer_id', 'customer_name', 'customer_address',
            'reference_id', 'amcname', 'invoice_frequency','latitude', 
            'amc_type', 'amc_type_name', 'payment_terms', 
            'payment_terms_name', 'start_date', 'end_date', 
            'equipment_no', 'notes', 'is_generate_contract',
            'no_of_services', 'price', 'no_of_lifts', 
            'gst_percentage', 'total', 'contract_amount', 
            'total_amount_paid', 'amount_due', 'status', 
            'amc_service_item', 'amc_service_item_name','created','created_display'
        ]

    def validate(self, data):
     today = timezone.now().date()
     is_renewal = self.context.get('is_renewal', False)

    # Rule 1: Start date must be today or later
     if 'start_date' in data and data['start_date']:
            if data['start_date'] < today and not is_renewal:
                raise serializers.ValidationError({
                    "start_date": f"Start date cannot be before {today} unless renewing an expired AMC."
                })

    # Rule 2: End date must be after start date
     if data.get('end_date') and data.get('start_date'):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })

    # Rule 3: No of services must be positive (only if provided)
     if data.get('no_of_services') is not None:
        if data['no_of_services'] <= 0:
            raise serializers.ValidationError({
                "no_of_services": "Number of services must be greater than zero."
            })

    # Rule 4: Price, Lifts, GST must be non-negative (only if provided)
     if data.get('price') is not None and data['price'] < 0:
        raise serializers.ValidationError({"price": "Price cannot be negative."})
     if data.get('no_of_lifts') is not None and data['no_of_lifts'] < 0:
        raise serializers.ValidationError({"no_of_lifts": "Number of lifts cannot be negative."})
     if data.get('gst_percentage') is not None and data['gst_percentage'] < 0:
        raise serializers.ValidationError({"gst_percentage": "GST percentage cannot be negative."})
        # Ensure customer is valid

     if 'customer' not in data or data['customer'] is None:
            raise serializers.ValidationError({
                "customer": "A valid customer is required."
            })

     return data

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')

        # Default end_date = start_date + 1 year (if not provided)
        if start_date and not end_date:
            validated_data['end_date'] = start_date + timedelta(days=365)

        # 🆕 auto-fill latitude from customer.site_address if not provided
        if not validated_data.get("latitude"):
            validated_data["latitude"] = customer.site_address

        return AMC.objects.create(customer=customer, **validated_data)

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer', None)
        if customer_data:
            instance.customer = customer_data

        start_date = validated_data.get('start_date', instance.start_date)
        end_date = validated_data.get('end_date')

        # Default end_date = start_date + 1 year (if not provided in update)
        if start_date and not end_date:
            validated_data['end_date'] = start_date + timedelta(days=365)

        # 🆕 auto-update latitude if not manually provided
        if customer_data and not validated_data.get("latitude"):
            validated_data["latitude"] = customer_data.site_address

        return super().update(instance, validated_data)

    def get_created_display(self, obj):
        return obj.created.strftime("%d-%m-%Y %H:%M")  # Format: 31-12-2023 14:30