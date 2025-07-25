from rest_framework import serializers
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin

# Existing serializers for related models (unchanged)
class FloorIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorID
        fields = ['id', 'value']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'value']

class MachineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineType
        fields = ['id', 'value']

class MachineBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineBrand
        fields = ['id', 'value']

class DoorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorType
        fields = ['id', 'value']

class DoorBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorBrand
        fields = ['id', 'value']

class LiftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiftType
        fields = ['id', 'value']

class ControllerBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControllerBrand
        fields = ['id', 'value']

class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = ['id', 'value']

# Modified LiftSerializer
class LiftSerializer(serializers.ModelSerializer):
    # Keep PrimaryKeyRelatedField for write operations (e.g., POST, PUT)
    floor_id = serializers.PrimaryKeyRelatedField(queryset=FloorID.objects.all(), write_only=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), write_only=True)
    lift_type = serializers.PrimaryKeyRelatedField(queryset=LiftType.objects.all(), write_only=True)
    machine_type = serializers.PrimaryKeyRelatedField(queryset=MachineType.objects.all(), write_only=True)
    machine_brand = serializers.PrimaryKeyRelatedField(queryset=MachineBrand.objects.all(), write_only=True)
    door_type = serializers.PrimaryKeyRelatedField(queryset=DoorType.objects.all(), write_only=True)
    door_brand = serializers.PrimaryKeyRelatedField(queryset=DoorBrand.objects.all(), write_only=True)
    controller_brand = serializers.PrimaryKeyRelatedField(queryset=ControllerBrand.objects.all(), write_only=True)
    cabin = serializers.PrimaryKeyRelatedField(queryset=Cabin.objects.all(), write_only=True)

    # Use SerializerMethodField for read operations to return only the 'value' field
    floor_id_value = serializers.SerializerMethodField()
    brand_value = serializers.SerializerMethodField()
    lift_type_value = serializers.SerializerMethodField()
    machine_type_value = serializers.SerializerMethodField()
    machine_brand_value = serializers.SerializerMethodField()
    door_type_value = serializers.SerializerMethodField()
    door_brand_value = serializers.SerializerMethodField()
    controller_brand_value = serializers.SerializerMethodField()
    cabin_value = serializers.SerializerMethodField()

    class Meta:
        model = Lift
        fields = [
            'id', 'lift_code', 'name', 'price', 'model', 'no_of_passengers', 'load_kg', 'speed',
            'floor_id_value', 'brand_value', 'lift_type_value', 'machine_type_value',
            'machine_brand_value', 'door_type_value', 'door_brand_value',
            'controller_brand_value', 'cabin_value',
            # Include write-only fields for POST/PUT
            'floor_id', 'brand', 'lift_type', 'machine_type', 'machine_brand',
            'door_type', 'door_brand', 'controller_brand', 'cabin'
        ]

    # Define methods to get the 'value' field for each related model
    def get_floor_id_value(self, obj):
        return obj.floor_id.value if obj.floor_id else None

    def get_brand_value(self, obj):
        return obj.brand.value if obj.brand else None

    def get_lift_type_value(self, obj):
        return obj.lift_type.value if obj.lift_type else None

    def get_machine_type_value(self, obj):
        return obj.machine_type.value if obj.machine_type else None

    def get_machine_brand_value(self, obj):
        return obj.machine_brand.value if obj.machine_brand else None

    def get_door_type_value(self, obj):
        return obj.door_type.value if obj.door_type else None

    def get_door_brand_value(self, obj):
        return obj.door_brand.value if obj.door_brand else None

    def get_controller_brand_value(self, obj):
        return obj.controller_brand.value if obj.controller_brand else None

    def get_cabin_value(self, obj):
        return obj.cabin.value if obj.cabin else None