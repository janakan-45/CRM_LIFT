from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin,Type, Make, Unit, Item
from .serializers import LiftSerializer, FloorIDSerializer, BrandSerializer, MachineTypeSerializer, MachineBrandSerializer, DoorTypeSerializer, DoorBrandSerializer, LiftTypeSerializer, ControllerBrandSerializer, CabinSerializer,TypeSerializer, MakeSerializer, UnitSerializer, ItemSerializer
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO

############################lift ######################################
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

@api_view(['GET'])
def export_lifts_to_excel(request):
    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Lifts"

    # Define headers
    headers = [
        'Lift Code', 'Name', 'Price', 'Model', 'No of Passengers', 'Load (kg)', 'Speed',
        'Floor ID', 'Brand', 'Lift Type', 'Machine Type', 'Machine Brand',
        'Door Type', 'Door Brand', 'Controller Brand', 'Cabin'
    ]
    
    # Write headers to the first row
    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header
    
    # Fetch all lifts
    lifts = Lift.objects.all()
    
    # Write lift data
    for row_num, lift in enumerate(lifts, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = lift.lift_code
        ws[f"{get_column_letter(2)}{row_num}"] = lift.name
        ws[f"{get_column_letter(3)}{row_num}"] = float(lift.price)  # Convert Decimal to float
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
    
    # Create a BytesIO buffer to store the Excel file
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Create the HTTP response with the Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=lifts_export.xlsx'
    response.write(output.read())
    
    return response






########################items########################################








@api_view(['POST'])
def add_type(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_make(request):
    serializer = MakeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_unit(request):
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_types(request):
    types = Type.objects.all()
    serializer = TypeSerializer(types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_makes(request):
    makes = Make.objects.all()
    serializer = MakeSerializer(makes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_units(request):
    units = Unit.objects.all()
    serializer = UnitSerializer(units, many=True)
    return Response(serializer.data)

@api_view(['POST'])
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
def item_list(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
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
def delete_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response({"message": "Item deleted successfully!"}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def export_items_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Items"

    headers = [
        'Item Number', 'Name', 'Make', 'Model', 'Type', 'Capacity', 'Threshold Qty',
        'Sale Price', 'Purchase Price', 'Service Type', 'Tax Preference', 'Unit',
        'SAC Code', 'HSN/HAC Code', 'IGST', 'GST', 'Description'
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
        ws[f"{get_column_letter(9)}{row_num}"] = float(item.purchase_price)
        ws[f"{get_column_letter(10)}{row_num}"] = item.service_type
        ws[f"{get_column_letter(11)}{row_num}"] = item.tax_preference
        ws[f"{get_column_letter(12)}{row_num}"] = item.unit.value if item.unit else ''
        ws[f"{get_column_letter(13)}{row_num}"] = item.sac_code if item.sac_code else ''
        ws[f"{get_column_letter(14)}{row_num}"] = item.hsn_hac_code if item.hsn_hac_code else ''
        ws[f"{get_column_letter(15)}{row_num}"] = float(item.igst) if item.igst else ''
        ws[f"{get_column_letter(16)}{row_num}"] = float(item.gst) if item.gst else ''
        ws[f"{get_column_letter(17)}{row_num}"] = item.description
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=items_export.xlsx'
    response.write(output.read())
    
    return response