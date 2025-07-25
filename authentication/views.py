from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin
from .serializers import LiftSerializer, FloorIDSerializer, BrandSerializer, MachineTypeSerializer, MachineBrandSerializer, DoorTypeSerializer, DoorBrandSerializer, LiftTypeSerializer, ControllerBrandSerializer, CabinSerializer

@api_view(['POST'])
def add_floor_id(request):
    serializer = FloorIDSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_brand(request):
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_machine_type(request):
    serializer = MachineTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_machine_brand(request):
    serializer = MachineBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_door_type(request):
    serializer = DoorTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_door_brand(request):
    serializer = DoorBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_lift_type(request):
    serializer = LiftTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_controller_brand(request):
    serializer = ControllerBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_cabin(request):
    serializer = CabinSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_floor_ids(request):
    floor_ids = FloorID.objects.all()
    serializer = FloorIDSerializer(floor_ids, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_machine_types(request):
    machine_types = MachineType.objects.all()
    serializer = MachineTypeSerializer(machine_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_machine_brands(request):
    machine_brands = MachineBrand.objects.all()
    serializer = MachineBrandSerializer(machine_brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_door_types(request):
    door_types = DoorType.objects.all()
    serializer = DoorTypeSerializer(door_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_door_brands(request):
    door_brands = DoorBrand.objects.all()
    serializer = DoorBrandSerializer(door_brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_lift_types(request):
    lift_types = LiftType.objects.all()
    serializer = LiftTypeSerializer(lift_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_controller_brands(request):
    controller_brands = ControllerBrand.objects.all()
    serializer = ControllerBrandSerializer(controller_brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_cabins(request):
    cabins = Cabin.objects.all()
    serializer = CabinSerializer(cabins, many=True)
    return Response(serializer.data)

@api_view(['POST'])
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
def delete_lift(request, pk):
    try:
        lift = Lift.objects.get(pk=pk)
        lift.delete()
        return Response({"message": "Lift deleted successfully!"}, status=status.HTTP_200_OK)
    except Lift.DoesNotExist:
        return Response({"error": "Lift not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lift_list(request):
    lifts = Lift.objects.all()
    serializer = LiftSerializer(lifts, many=True)
    return Response(serializer.data)