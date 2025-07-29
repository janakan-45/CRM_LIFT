from rest_framework import serializers
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin,Complaint, Employee,Customer


from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        # Check for existing username
        if User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})

        # Check for existing email
        if User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


# ###########################lift#######################################
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
    


#####################################items########################################

from rest_framework import serializers
from .models import Type, Make, Unit, Item

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'value']

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'value']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'value']

class ItemSerializer(serializers.ModelSerializer):
    make = serializers.PrimaryKeyRelatedField(queryset=Make.objects.all(), write_only=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), write_only=True)
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), write_only=True)
    make_value = serializers.SerializerMethodField()
    type_value = serializers.SerializerMethodField()
    unit_value = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'item_number', 'name', 'make_value', 'model', 'type_value', 'capacity',
            'threshold_qty', 'sale_price', 'purchase_price', 'service_type', 'tax_preference',
            'unit_value', 'sac_code', 'hsn_hac_code', 'igst', 'gst', 'description',
            'make', 'type', 'unit'
        ]

    def get_make_value(self, obj):
        return obj.make.value if obj.make else None

    def get_type_value(self, obj):
        return obj.type.value if obj.type else None

    def get_unit_value(self, obj):
        return obj.unit.value if obj.unit else None

    def validate(self, data):
        if data['service_type'] == 'Goods' and not data.get('hsn_hac_code'):
            raise serializers.ValidationError("HSN/HAC Code is required for Goods.")
        if data['service_type'] == 'Services' and data['tax_preference'] == 'Taxable' and not (data.get('igst') or data.get('gst')):
            raise serializers.ValidationError("IGST or GST is required for Taxable Services.")
        if data['service_type'] == 'Services' and data['tax_preference'] == 'Non-Taxable' and (data.get('igst') or data.get('gst')):
            raise serializers.ValidationError("IGST and GST should not be set for Non-Taxable Services.")
        return data

    def create(self, validated_data):
        if validated_data['service_type'] == 'Goods':
            validated_data.pop('sac_code', None)
            validated_data.pop('igst', None)
            validated_data.pop('gst', None)
        elif validated_data['service_type'] == 'Services' and validated_data['tax_preference'] == 'Non-Taxable':
            validated_data.pop('sac_code', None)
            validated_data.pop('igst', None)
            validated_data.pop('gst', None)
        return super().create(validated_data)
    



##################################complaints########################################

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']

class ComplaintSerializer(serializers.ModelSerializer):
    assign_to = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), write_only=True, required=False)
    assign_to_name = serializers.SerializerMethodField()
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), write_only=True, required=False)
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = ['id', 'reference', 'type', 'date', 'customer_name', 'contact_person_name', 
                  'contact_person_mobile', 'block_wing', 'assign_to_name', 'priority', 
                  'subject', 'message', 'customer_signature', 'technician_remark', 
                  'technician_signature', 'solution', 'customer', 'assign_to']

    def get_assign_to_name(self, obj):
        return obj.assign_to.name if obj.assign_to else None

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None