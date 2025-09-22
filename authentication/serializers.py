from rest_framework import serializers
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin,Complaint, Employee,Customer,Profile,CustomUser


from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.conf import settings

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
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        if User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
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
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data


from django.core.files.images import get_image_dimensions

from rest_framework import serializers
from django.conf import settings
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'phone', 'photo']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.photo:
            request = self.context.get('request')
            if request:
                # absolute URL for frontend
                data['photo'] = request.build_absolute_uri(instance.photo.url)
            else:
                data['photo'] = settings.MEDIA_URL + str(instance.photo)
        else:
            data['photo'] = None
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        if 'username' in user_data:
            if User.objects.filter(username__iexact=user_data['username']).exclude(id=user.id).exists():
                raise serializers.ValidationError({"username": "This username is already taken."})
            user.username = user_data['username']

        if 'email' in user_data:
            if User.objects.filter(email__iexact=user_data['email']).exclude(id=user.id).exists():
                raise serializers.ValidationError({"email": "This email is already in use."})
            user.email = user_data['email']

        user.save()
        return super().update(instance, validated_data)


# In serializers.py

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match."})
        return data

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value


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

    def validate_lift_code(self, value):
        """
        Validate that the lift_code is unique.
        For updates, exclude the current instance from the uniqueness check.
        """
        instance = self.instance
        if instance and instance.lift_code == value:
            return value  # No change to lift_code, so no need to check uniqueness

        if Lift.objects.filter(lift_code=value).exists():
            raise serializers.ValidationError("A lift with this lift code already exists.")
        return value

    def validate(self, data):
        """
        Validate that load_kg matches no_of_passengers * 68.
        Extract the numeric part from no_of_passengers (e.g., '5 Persons' -> 5).
        """
        no_of_passengers = data.get('no_of_passengers', '')
        load_kg = data.get('load_kg', '')

        # Extract number of passengers (assuming format like "5 Persons")
        try:
            passengers = int(no_of_passengers.split()[0])
        except (ValueError, IndexError):
            raise serializers.ValidationError({
                'no_of_passengers': 'Invalid format. Expected format: "X Persons".'
            })

        # Calculate expected load
        expected_load = str(passengers * 68)  # Convert to string to match CharField

        # Validate load_kg
        if load_kg != expected_load:
            raise serializers.ValidationError({
                'load_kg': f'Load must be {expected_load} kg for {no_of_passengers}.'
            })

        return data

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
            'threshold_qty', 'sale_price', 'service_type', 'tax_preference',
            'unit_value', 'sac_code', 'igst', 'gst', 'description',
            'make', 'type', 'unit'
        ]
        extra_kwargs = {
            'item_number': {'read_only': True},  # Mark item_number as read-only since it's auto-generated
        }

    def get_make_value(self, obj):
        return obj.make.value if obj.make else None

    def get_type_value(self, obj):
        return obj.type.value if obj.type else None

    def get_unit_value(self, obj):
        return obj.unit.value if obj.unit else None

    def validate(self, data):
        if data['service_type'] == 'Services' and data['tax_preference'] == 'Taxable' and not (data.get('igst') or data.get('gst')):
            raise serializers.ValidationError({"tax": "IGST or GST is required for Taxable Services."})
        if data['service_type'] == 'Services' and data['tax_preference'] == 'Non-Taxable' and (data.get('igst') or data.get('gst')):
            raise serializers.ValidationError({"tax": "IGST and GST should not be set for Non-Taxable Services."})
        return data


    def create(self, validated_data):
        if validated_data['service_type'] == 'Goods':
            validated_data.pop('sac_code', None)
        elif validated_data['service_type'] == 'Services' and validated_data['tax_preference'] == 'Non-Taxable':
            validated_data.pop('sac_code', None)
            validated_data.pop('igst', None)
            validated_data.pop('gst', None)
        return super().create(validated_data)



##################################complaints########################################
class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser  # ✅ Use CustomUser instead of old Employee
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'role']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'role': {'required': True}  # role will be SALESMAN for employees
        }

    def validate(self, data):
        # Password match validation
        if 'password' in data and 'password_confirm' in data:
            if data['password'] != data['password_confirm']:
                raise serializers.ValidationError({"password": "Passwords must match."})

        # Username uniqueness
        if 'username' in data and CustomUser.objects.filter(username__iexact=data['username']).exists():
            if not (self.instance and self.instance.username == data['username']):
                raise serializers.ValidationError({"username": "An employee with this username already exists."})

        # Email uniqueness
        if 'email' in data and CustomUser.objects.filter(email__iexact=data['email']).exists():
            if not (self.instance and self.instance.email == data['email']):
                raise serializers.ValidationError({"email": "An employee with this email already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        # Force role to SALESMAN
        validated_data['role'] = 'SALESMAN'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # 🔥 use set_password
        return super().update(instance, validated_data)
    
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
        return obj.customer.site_name if obj.customer else None
    
        
# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

# ---------------- Register (Admin Request) ----------------
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

# ---------------- Approve Admin ----------------
class AdminApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role', 'is_active']

# ---------------- User Profile ----------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']

# ---------------- Login ----------------
# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from authentication.models import CustomUser

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate using email backend
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data

