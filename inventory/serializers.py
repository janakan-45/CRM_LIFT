from rest_framework import serializers
from .models import Requisition
from authentication.models import CustomUser  # ✅ use CustomUser now
from inventory.models import Item
from sales.models import Customer
from amc.models import AMC

####################################### Requisition Serializers ##########################################

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_number', 'name']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'reference_id', 'site_name']


class AMCSerializer(serializers.ModelSerializer):
    class Meta:
        model = AMC
        fields = ['id', 'amcname']  # make sure this field exists in AMC


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  # ✅ CustomUser fields (no "name" field by default)


class RequisitionSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    site = CustomerSerializer(read_only=True)
    amc_id = AMCSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    # Write-only fields for POST/PUT
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), write_only=True)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True)
    amc_pk = serializers.PrimaryKeyRelatedField(queryset=AMC.objects.all(), write_only=True, allow_null=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role="SALESMAN"),  # ✅ filter to SALESMAN
        write_only=True
    )

    class Meta:
        model = Requisition
        fields = [
            'id', 'reference_id', 'date', 'item', 'qty',
            'site', 'amc_id', 'service', 'employee',
            'item_id', 'site_id', 'amc_pk', 'employee_id',
            'status', 'approve_for'
        ]

    def create(self, validated_data):
        item = validated_data.pop('item_id')
        site = validated_data.pop('site_id')
        amc = validated_data.pop('amc_pk', None)
        employee = validated_data.pop('employee_id')

        requisition = Requisition.objects.create(
            date=validated_data.get('date'),
            item=item,
            qty=validated_data.get('qty'),
            site=site,
            amc_id=amc,
            service=validated_data.get('service', ''),
            employee=employee,
            status=validated_data.get('status', 'OPEN'),
            approve_for=validated_data.get('approve_for', 'PENDING')
        )
        return requisition

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.item = validated_data.get('item_id', instance.item)
        instance.qty = validated_data.get('qty', instance.qty)
        instance.site = validated_data.get('site_id', instance.site)
        instance.amc_id = validated_data.get('amc_pk', instance.amc_id)
        instance.service = validated_data.get('service', instance.service)
        instance.employee = validated_data.get('employee_id', instance.employee)
        instance.status = validated_data.get('status', instance.status)
        instance.approve_for = validated_data.get('approve_for', instance.approve_for)
        instance.save()
        return instance
