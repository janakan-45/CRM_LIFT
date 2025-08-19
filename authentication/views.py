from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin, Type, Make, Unit, Item,Complaint, Employee,Profile
from .serializers import LiftSerializer, FloorIDSerializer, BrandSerializer, MachineTypeSerializer, MachineBrandSerializer, DoorTypeSerializer, DoorBrandSerializer, LiftTypeSerializer, ControllerBrandSerializer, CabinSerializer, TypeSerializer, MakeSerializer, UnitSerializer, ItemSerializer, UserRegistrationSerializer, UserLoginSerializer,ComplaintSerializer, EmployeeSerializer,ResetPasswordSerializer,ForgotPasswordSerializer,ProfileSerializer
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
User = get_user_model()
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.parsers import MultiPartParser, FormParser


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='owner').exists()


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwner])
def check_owner_status(request):
    user = request.user
    return Response({
        'message': f'User {user.username} is an owner',
        'is_owner': True
    }, status=status.HTTP_200_OK)


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='employee').exists()
    

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsEmployee])
def check_employee_status(request):
    user = request.user
    return Response({
        'message': f'User {user.username} is an employee',
        'is_employee': True
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Check if owner group exists, create if it doesn't
        owner_group, created = Group.objects.get_or_create(name='owner')
        
        # Assign user to owner group
        user.groups.add(owner_group)
        
        refresh = RefreshToken.for_user(user)

        # Send confirmation email
        subject = 'Welcome to ATOM LIFT - Registration Successful'
        message = (
            f"Dear {user.username},\n\n"
            "Thank you for registering with ATOM LIFT!\n"
            "Your account has been successfully created with owner privileges.\n\n"
            "You can now log in using your email and password.\n"
            "If you have any questions, feel free to contact us.\n\n"
            "Best regards,\n"
            "The ATOM LIFT Team"
        )
        from_email = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>"
        recipient_list = [user.email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            # Log the error if needed, but don't fail the registration
            print(f"Failed to send email: {str(e)}")

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data,
            'message': 'Registration successful! A confirmation email has been sent to your email address.'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        # Authenticate using email
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)

            # Get the user's group(s)
            groups = [group.name for group in user.groups.all()]

            # Send login notification email
            login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
            subject = 'ATOM LIFT - Successful Login Notification'
            message = (
                f"Dear {user.username},\n\n"
                "You have successfully logged in to your ATOM LIFT account.\n\n"
                f"Login Time: {login_time}\n"
                "If this was not you, please secure your account immediately by changing your password.\n\n"
                "Best regards,\n"
                "The ATOM LIFT Team"
            )
            from_email = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>"
            recipient_list = [user.email]

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error if needed, but don't fail the login
                print(f"Failed to send login email: {str(e)}")

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'groups': groups,  # Include the user's group(s)
                },
                'message': 'Login successful! A notification email has been sent to your email address.'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email__iexact=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construct reset link (adjust the frontend URL as needed)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        
        # Send password reset email
        subject = 'ATOM LIFT - Password Reset Request'
        message = (
            f"Dear {user.username},\n\n"
            "You have requested to reset your password for your ATOM LIFT account.\n"
            f"Please click the following link to reset your password:\n\n"
            f"{reset_url}\n\n"
            "This link is valid for 1 hour. If you did not request a password reset, please ignore this email.\n\n"
            "Best regards,\n"
            "The ATOM LIFT Team"
        )
        from_email = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>"
        recipient_list = [user.email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send password reset email: {str(e)}")
            return Response({'error': 'Failed to send password reset email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': 'Password reset email sent successfully.'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        
        try:
            from django.utils.http import urlsafe_base64_decode
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({
                'message': 'Password reset successfully.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        profile = request.user.profile
        print(f"Profile found: {profile}")
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        print(f"Created new profile for user: {request.user}")
    
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    parser_classes = (MultiPartParser, FormParser)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################ Lift ######################################

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_floor_id(request):
    serializer = FloorIDSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_floor_id(request, pk):
    try:
        floor_id = FloorID.objects.get(pk=pk)
    except FloorID.DoesNotExist:
        return Response({"error": "FloorID not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = FloorIDSerializer(floor_id, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "FloorID updated successfully!",
            "floor_id": floor_id.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_floor_id(request, pk):
    try:
        floor_id = FloorID.objects.get(pk=pk)
        floor_id.delete()
        return Response({"message": "FloorID deleted successfully!"}, status=status.HTTP_200_OK)
    except FloorID.DoesNotExist:
        return Response({"error": "FloorID not found"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_brand(request):
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_brand(request, pk):
    try:
        brand = Brand.objects.get(pk=pk)
    except Brand.DoesNotExist:
        return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BrandSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Brand updated successfully!",
            "brand_id": brand.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_brand(request, pk):
    try:
        brand = Brand.objects.get(pk=pk)
        brand.delete()
        return Response({"message": "Brand deleted successfully!"}, status=status.HTTP_200_OK)
    except Brand.DoesNotExist:
        return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_machine_type(request):
    serializer = MachineTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_machine_type(request, pk):
    try:
        machine_type = MachineType.objects.get(pk=pk)
    except MachineType.DoesNotExist:
        return Response({"error": "MachineType not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MachineTypeSerializer(machine_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "MachineType updated successfully!",
            "machine_type_id": machine_type.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_machine_type(request, pk):
    try:
        machine_type = MachineType.objects.get(pk=pk)
        machine_type.delete()
        return Response({"message": "MachineType deleted successfully!"}, status=status.HTTP_200_OK)
    except MachineType.DoesNotExist:
        return Response({"error": "MachineType not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_machine_brand(request):
    serializer = MachineBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_machine_brand(request, pk):
    try:
        machine_brand = MachineBrand.objects.get(pk=pk)
    except MachineBrand.DoesNotExist:
        return Response({"error": "MachineBrand not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MachineBrandSerializer(machine_brand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "MachineBrand updated successfully!",
            "machine_brand_id": machine_brand.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_machine_brand(request, pk):
    try:
        machine_brand = MachineBrand.objects.get(pk=pk)
        machine_brand.delete()
        return Response({"message": "MachineBrand deleted successfully!"}, status=status.HTTP_200_OK)
    except MachineBrand.DoesNotExist:
        return Response({"error": "MachineBrand not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_door_type(request):
    serializer = DoorTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_door_type(request, pk):
    try:
        door_type = DoorType.objects.get(pk=pk)
    except DoorType.DoesNotExist:
        return Response({"error": "DoorType not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoorTypeSerializer(door_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "DoorType updated successfully!",
            "door_type_id": door_type.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_door_type(request, pk):
    try:
        door_type = DoorType.objects.get(pk=pk)
        door_type.delete()
        return Response({"message": "DoorType deleted successfully!"}, status=status.HTTP_200_OK)
    except DoorType.DoesNotExist:
        return Response({"error": "DoorType not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_door_brand(request):
    serializer = DoorBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_door_brand(request, pk):
    try:
        door_brand = DoorBrand.objects.get(pk=pk)
    except DoorBrand.DoesNotExist:
        return Response({"error": "DoorBrand not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoorBrandSerializer(door_brand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "DoorBrand updated successfully!",
            "door_brand_id": door_brand.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_door_brand(request, pk):
    try:
        door_brand = DoorBrand.objects.get(pk=pk)
        door_brand.delete()
        return Response({"message": "DoorBrand deleted successfully!"}, status=status.HTTP_200_OK)
    except DoorBrand.DoesNotExist:
        return Response({"error": "DoorBrand not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_lift_type(request):
    serializer = LiftTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_lift_type(request, pk):
    try:
        lift_type = LiftType.objects.get(pk=pk)
    except LiftType.DoesNotExist:
        return Response({"error": "LiftType not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = LiftTypeSerializer(lift_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "LiftType updated successfully!",
            "lift_type_id": lift_type.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_lift_type(request, pk):
    try:
        lift_type = LiftType.objects.get(pk=pk)
        lift_type.delete()
        return Response({"message": "LiftType deleted successfully!"}, status=status.HTTP_200_OK)
    except LiftType.DoesNotExist:
        return Response({"error": "LiftType not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_controller_brand(request):
    serializer = ControllerBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_controller_brand(request, pk):
    try:
        controller_brand = ControllerBrand.objects.get(pk=pk)
    except ControllerBrand.DoesNotExist:
        return Response({"error": "ControllerBrand not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ControllerBrandSerializer(controller_brand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "ControllerBrand updated successfully!",
            "controller_brand_id": controller_brand.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_controller_brand(request, pk):
    try:
        controller_brand = ControllerBrand.objects.get(pk=pk)
        controller_brand.delete()
        return Response({"message": "ControllerBrand deleted successfully!"}, status=status.HTTP_200_OK)
    except ControllerBrand.DoesNotExist:
        return Response({"error": "ControllerBrand not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_cabin(request):
    serializer = CabinSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_cabin(request, pk):
    try:
        cabin = Cabin.objects.get(pk=pk)
    except Cabin.DoesNotExist:
        return Response({"error": "Cabin not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CabinSerializer(cabin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Cabin updated successfully!",
            "cabin_id": cabin.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_cabin(request, pk):
    try:
        cabin = Cabin.objects.get(pk=pk)
        cabin.delete()
        return Response({"message": "Cabin deleted successfully!"}, status=status.HTTP_200_OK)
    except Cabin.DoesNotExist:
        return Response({"error": "Cabin not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_floor_ids(request):
    floor_ids = FloorID.objects.all()
    serializer = FloorIDSerializer(floor_ids, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_machine_types(request):
    machine_types = MachineType.objects.all()
    serializer = MachineTypeSerializer(machine_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_machine_brands(request):
    machine_brands = MachineBrand.objects.all()
    serializer = MachineBrandSerializer(machine_brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_door_types(request):
    door_types = DoorType.objects.all()
    serializer = DoorTypeSerializer(door_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_door_brands(request):
    door_brands = DoorBrand.objects.all()
    serializer = DoorBrandSerializer(door_brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lift_types(request):
    lift_types = LiftType.objects.all()
    serializer = LiftTypeSerializer(lift_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_controller_brands(request):
    controller_brands = ControllerBrand.objects.all()
    serializer = ControllerBrandSerializer(controller_brands, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cabins(request):
    cabins = Cabin.objects.all()
    serializer = CabinSerializer(cabins, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lift(request):
    serializer = LiftSerializer(data=request.data)
    if serializer.is_valid():
        lift = serializer.save()
        return Response({
            "message": "Lift added successfully!",
            "lift_id": lift.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_lift(request, pk):
    try:
        lift = Lift.objects.get(pk=pk)
    except Lift.DoesNotExist:
        return Response({"error": "Lift not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LiftSerializer(lift, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Lift updated successfully!",
            "lift_id": lift.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lift(request, pk):
    try:
        lift = Lift.objects.get(pk=pk)
        lift.delete()
        return Response({"message": "Lift deleted successfully!"}, status=status.HTTP_200_OK)
    except Lift.DoesNotExist:
        return Response({"error": "Lift not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lift_list(request):
    lifts = Lift.objects.all()
    serializer = LiftSerializer(lifts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_lifts_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lifts"

    headers = [
        'Lift Code', 'Name', 'Price', 'Model', 'No of Passengers', 'Load (kg)', 'Speed',
        'Floor ID', 'Brand', 'Lift Type', 'Machine Type', 'Machine Brand',
        'Door Type', 'Door Brand', 'Controller Brand', 'Cabin'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    lifts = Lift.objects.all()

    for row_num, lift in enumerate(lifts, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = lift.lift_code
        ws[f"{get_column_letter(2)}{row_num}"] = lift.name
        ws[f"{get_column_letter(3)}{row_num}"] = float(lift.price)
        ws[f"{get_column_letter(4)}{row_num}"] = lift.model
        ws[f"{get_column_letter(5)}{row_num}"] = lift.no_of_passengers
        ws[f"{get_column_letter(6)}{row_num}"] = lift.load_kg
        ws[f"{get_column_letter(7)}{row_num}"] = lift.speed
        ws[f"{get_column_letter(8)}{row_num}"] = lift.floor_id.value if lift.floor_id else ''
        ws[f"{get_column_letter(9)}{row_num}"] = lift.brand.value if lift.brand else ''
        ws[f"{get_column_letter(10)}{row_num}"] = lift.lift_type.value if lift.lift_type else ''
        ws[f"{get_column_letter(11)}{row_num}"] = lift.machine_type.value if lift.machine_type else ''
        ws[f"{get_column_letter(12)}{row_num}"] = lift.machine_brand.value if lift.machine_brand else ''
        ws[f"{get_column_letter(13)}{row_num}"] = lift.door_type.value if lift.door_type else ''
        ws[f"{get_column_letter(14)}{row_num}"] = lift.door_brand.value if lift.door_brand else ''
        ws[f"{get_column_letter(15)}{row_num}"] = lift.controller_brand.value if lift.controller_brand else ''
        ws[f"{get_column_letter(16)}{row_num}"] = lift.cabin.value if lift.cabin else ''

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=lifts_export.xlsx'
    response.write(output.read())

    return response

import csv
import io


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_lifts_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return Response({"error": "File is not a CSV"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=',')
        next(reader)  # Skip header row
        for row in reader:
            if not row:  # Skip blank rows
                continue
            if any(',' in field for field in row):  # Check for commas in data
                return Response({"error": "CSV contains commas in data"}, status=status.HTTP_400_BAD_REQUEST)

            # Map CSV columns to Lift model fields
            # Assuming CSV order: lift_code, name, price, model, no_of_passengers, load_kg, speed,
            # floor_id_value, brand_value, lift_type_value, machine_type_value, machine_brand_value,
            # door_type_value, door_brand_value, controller_brand_value, cabin_value
            lift_data = {
                'lift_code': row[0],
                'name': row[1],
                'price': float(row[2]) if row[2] else 0.00,
                'model': row[3],
                'no_of_passengers': row[4],
                'load_kg': row[5],
                'speed': row[6],
                # Map foreign key values to their IDs based on 'value' fields
                'floor_id': FloorID.objects.get_or_create(value=row[7])[0],
                'brand': Brand.objects.get_or_create(value=row[8])[0],
                'lift_type': LiftType.objects.get_or_create(value=row[9])[0],
                'machine_type': MachineType.objects.get_or_create(value=row[10])[0],
                'machine_brand': MachineBrand.objects.get_or_create(value=row[11])[0],
                'door_type': DoorType.objects.get_or_create(value=row[12])[0],
                'door_brand': DoorBrand.objects.get_or_create(value=row[13])[0],
                'controller_brand': ControllerBrand.objects.get_or_create(value=row[14])[0],
                'cabin': Cabin.objects.get_or_create(value=row[15])[0],
            }
            serializer = LiftSerializer(data=lift_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Lifts imported successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




############################ Items ######################################


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_type(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_type(request, pk):
    try:
        type_obj = Type.objects.get(pk=pk)
    except Type.DoesNotExist:
        return Response({"error": "Type not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TypeSerializer(type_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Type updated successfully!",
            "type_id": type_obj.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_type(request, pk):
    try:
        type_obj = Type.objects.get(pk=pk)
        type_obj.delete()
        return Response({"message": "Type deleted successfully!"}, status=status.HTTP_200_OK)
    except Type.DoesNotExist:
        return Response({"error": "Type not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_make(request):
    serializer = MakeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_make(request, pk):
    try:
        make = Make.objects.get(pk=pk)
    except Make.DoesNotExist:
        return Response({"error": "Make not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MakeSerializer(make, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Make updated successfully!",
            "make_id": make.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_make(request, pk):
    try:
        make = Make.objects.get(pk=pk)
        make.delete()
        return Response({"message": "Make deleted successfully!"}, status=status.HTTP_200_OK)
    except Make.DoesNotExist:
        return Response({"error": "Make not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def add_unit(request):
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsOwner])
def edit_unit(request, pk):
    try:
        unit = Unit.objects.get(pk=pk)
    except Unit.DoesNotExist:
        return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UnitSerializer(unit, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Unit updated successfully!",
            "unit_id": unit.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsOwner])
def delete_unit(request, pk):
    try:
        unit = Unit.objects.get(pk=pk)
        unit.delete()
        return Response({"message": "Unit deleted successfully!"}, status=status.HTTP_200_OK)
    except Unit.DoesNotExist:
        return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_types(request):
    types = Type.objects.all()
    serializer = TypeSerializer(types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_makes(request):
    makes = Make.objects.all()
    serializer = MakeSerializer(makes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_units(request):
    units = Unit.objects.all()
    serializer = UnitSerializer(units, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        return Response({
            "message": "Item added successfully!",
            "item_id": item.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Item updated successfully!",
            "item_id": item.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response({"message": "Item deleted successfully!"}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_items_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Items"

    headers = [
        'Item Number', 'Name', 'Make', 'Model', 'Type', 'Capacity', 'Threshold Qty',
        'Sale Price', 'Service Type', 'Tax Preference', 'Unit',
        'SAC Code', 'IGST', 'GST', 'Description'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    items = Item.objects.all()

    for row_num, item in enumerate(items, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = item.item_number
        ws[f"{get_column_letter(2)}{row_num}"] = item.name
        ws[f"{get_column_letter(3)}{row_num}"] = item.make.value if item.make else ''
        ws[f"{get_column_letter(4)}{row_num}"] = item.model
        ws[f"{get_column_letter(5)}{row_num}"] = item.type.value if item.type else ''
        ws[f"{get_column_letter(6)}{row_num}"] = item.capacity
        ws[f"{get_column_letter(7)}{row_num}"] = item.threshold_qty
        ws[f"{get_column_letter(8)}{row_num}"] = float(item.sale_price)
        ws[f"{get_column_letter(9)}{row_num}"] = item.service_type
        ws[f"{get_column_letter(10)}{row_num}"] = item.tax_preference
        ws[f"{get_column_letter(11)}{row_num}"] = item.unit.value if item.unit else ''
        ws[f"{get_column_letter(12)}{row_num}"] = item.sac_code if item.sac_code else ''
        ws[f"{get_column_letter(13)}{row_num}"] = float(item.igst) if item.igst else ''
        ws[f"{get_column_letter(14)}{row_num}"] = float(item.gst) if item.gst else ''
        ws[f"{get_column_letter(15)}{row_num}"] = item.description

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=items_export.xlsx'
    response.write(output.read())

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_items_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return Response({"error": "File is not a CSV"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=',')
        next(reader)  # Skip header row
        for row in reader:
            if not row:  # Skip blank rows
                continue
            if any(',' in field or not field.isalnum() for field in row):  # Check for commas or special characters
                return Response({"error": "CSV contains commas or special characters"}, status=status.HTTP_400_BAD_REQUEST)

            # Map CSV columns to Item model fields
            # Assuming CSV order: item_number, name, make_value, model, type_value, capacity,
            # threshold_qty, sale_price, service_type, tax_preference, unit_value,
            # sac_code, igst, gst, description
            item_data = {
                'item_number': row[0],
                'name': row[1],
                'make': Make.objects.get_or_create(value=row[2])[0],
                'model': row[3],
                'type': Type.objects.get_or_create(value=row[4])[0],
                'capacity': row[5],
                'threshold_qty': int(row[6]) if row[6] else 0,
                'sale_price': float(row[7]) if row[7] else 0.00,
                'service_type': row[8] if row[8] in ['Services', 'Goods'] else 'Goods',
                'tax_preference': row[9] if row[9] in ['Non-Taxable', 'Taxable'] else 'Non-Taxable',
                'unit': Unit.objects.get_or_create(value=row[10])[0],
                'sac_code': row[11] if row[11] else None,
                'igst': float(row[12]) if row[12] else None,
                'gst': float(row[13]) if row[13] else None,
                'description': row[14] if row[14] else None,
            }
            serializer = ItemSerializer(data=item_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Items imported successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





####################################complaints########################################
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        plain_password = request.data.get('password')
        employee = serializer.save()
        
        try:
            user = User.objects.create_user(
                username=employee.username,
                email=employee.email,
                password=plain_password
            )
            employee_group, created = Group.objects.get_or_create(name='employee')
            user.groups.add(employee_group)
        except Exception as e:
            employee.delete()
            return Response({"error": f"Failed to create user account: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        subject = 'Welcome to ATOM LIFT - Employee Account Created'
        message = (
            f"Dear {employee.name},\n\n"
            "Your employee account has been successfully created with ATOM LIFT.\n\n"
            "You can now log in using your email and password.\n"
            "If you have any questions, feel free to contact us.\n\n"
            "Best regards,\n"
            "The ATOM LIFT Team"
        )
        from_email = f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_HOST_USER}>"
        recipient_list = [employee.email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

        return Response({
            "message": "Employee added successfully!",
            "employee_id": employee.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsOwner])
def edit_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        plain_password = request.data.get('password')
        employee = serializer.save()
        
        try:
            user = User.objects.get(email=employee.email)
            if 'username' in request.data:
                user.username = employee.username
            if 'email' in request.data:
                user.email = employee.email
            if plain_password:
                user.set_password(plain_password)
            user.save()
        except User.DoesNotExist:
            return Response({"error": "Associated user not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Failed to update user account: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "Employee updated successfully!",
            "employee_id": employee.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsOwner])
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        try:
            user = User.objects.get(email=employee.email)
            user.delete()
        except User.DoesNotExist:
            pass
        employee.delete()
        return Response({"message": "Employee deleted successfully!"}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_complaint(request):
    serializer = ComplaintSerializer(data=request.data)
    if serializer.is_valid():
        complaint = serializer.save()
        return Response({
            "message": "Complaint added successfully!",
            "complaint_id": complaint.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def complaint_list(request):
    complaints = Complaint.objects.all()
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_complaint(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk)
    except Complaint.DoesNotExist:
        return Response({"error": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ComplaintSerializer(complaint, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Complaint updated successfully!",
            "complaint_id": complaint.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_complaint(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk)
        complaint.delete()
        return Response({"message": "Complaint deleted successfully!"}, status=status.HTTP_200_OK)
    except Complaint.DoesNotExist:
        return Response({"error": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_complaints_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Complaints"

    headers = [
        'Reference', 'Type', 'Date', 'Customer Name', 'Contact Person Name',
        'Contact Person Mobile', 'Block/Wing', 'Assigned To', 'Priority',
        'Subject', 'Message'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    complaints = Complaint.objects.all()

    for row_num, complaint in enumerate(complaints, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = complaint.reference
        ws[f"{get_column_letter(2)}{row_num}"] = complaint.type
        ws[f"{get_column_letter(3)}{row_num}"] = complaint.date.strftime('%Y-%m-%d %H:%M:%S')
        ws[f"{get_column_letter(4)}{row_num}"] = complaint.customer.name if complaint.customer else ''
        ws[f"{get_column_letter(5)}{row_num}"] = complaint.contact_person_name
        ws[f"{get_column_letter(6)}{row_num}"] = complaint.contact_person_mobile
        ws[f"{get_column_letter(7)}{row_num}"] = complaint.block_wing
        ws[f"{get_column_letter(8)}{row_num}"] = complaint.assign_to.name if complaint.assign_to else ''
        ws[f"{get_column_letter(9)}{row_num}"] = complaint.priority
        ws[f"{get_column_letter(10)}{row_num}"] = complaint.subject
        ws[f"{get_column_letter(11)}{row_num}"] = complaint.message

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=complaints_export.xlsx'
    response.write(output.read())

    return response


from django.template.loader import get_template
from xhtml2pdf import pisa

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def print_complaint(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk)
    except Complaint.DoesNotExist:
        return Response({"error": "Complaint not found"}, status=status.HTTP_404_NOT_FOUND)

    # Prepare data for PDF
    context = {
        'company_name': 'Atom Lifts India Pvt Ltd',
        'address': 'No.87B, Pillayar Koll Street, Mannurpet, Ambattur Indus Estate, Chennai 50, CHENNAI',
        'phone': '9600087456',
        'email': 'admin@atomlifts.com',
        'ticket_no': complaint.reference,
        'ticket_date': complaint.date.strftime('%d/%m/%Y %H:%M:%S'),
        'ticket_type': complaint.type,
        'priority': complaint.priority,
        'customer_name': complaint.customer.name if complaint.customer else '',
        'site_address': f"{complaint.contact_person_name}, {complaint.contact_person_mobile}",
        'contact_person': complaint.contact_person_name,
        'contact_mobile': complaint.contact_person_mobile,
        'block_wing': complaint.block_wing,
        'subject': complaint.subject,
        'message': complaint.message,
        'assigned_to': complaint.assign_to.name if complaint.assign_to else '',
        'customer_signature': complaint.customer_signature,
        'technician_remark': complaint.technician_remark,
        'technician_signature': complaint.technician_signature,
        'solution': complaint.solution
    }

    # Load template and render PDF
    template = get_template('complaint_pdf.html')
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=complaint_{complaint.reference}.pdf'
        return response
    return HttpResponse("Error generating PDF", status=status.HTTP_500_INTERNAL_SERVER_ERROR)