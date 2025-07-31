from rest_framework import serializers
from .models import Requisition
from authentication.models import Item, Employee
from sales.models import Customer
from amc.models import AMC

#######################################requisition serializers##########################################

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
        fields = ['id', 'reference_id']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']

class RequisitionSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    site = CustomerSerializer()
    amc_id = AMCSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = Requisition
        fields = ['id', 'reference_id', 'date', 'item', 'qty', 'site', 'amc_id', 'service', 'employee']

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        site_data = validated_data.pop('site')
        amc_data = validated_data.pop('amc_id')
        employee_data = validated_data.pop('employee')

        item = Item.objects.get(id=item_data['id'])
        site = Customer.objects.get(id=site_data['id'])
        amc = AMC.objects.get(id=amc_data['id'])
        employee = Employee.objects.get(id=employee_data['id']) if employee_data.get('id') else None

        requisition = Requisition.objects.create(
            date=validated_data['date'],
            item=item,
            qty=validated_data['qty'],
            site=site,
            amc_id=amc,
            service=validated_data.get('service', ''),
            employee=employee
        )
        return requisition

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item')
        site_data = validated_data.pop('site')
        amc_data = validated_data.pop('amc_id')
        employee_data = validated_data.pop('employee')

        instance.date = validated_data.get('date', instance.date)
        instance.item = Item.objects.get(id=item_data['id'])
        instance.qty = validated_data.get('qty', instance.qty)
        instance.site = Customer.objects.get(id=site_data['id'])
        instance.amc_id = AMC.objects.get(id=amc_data['id'])
        instance.service = validated_data.get('service', instance.service)
        instance.employee = Employee.objects.get(id=employee_data['id']) if employee_data.get('id') else None
        instance.save()
        return instance