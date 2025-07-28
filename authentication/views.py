from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Lift, FloorID, Brand, MachineType, MachineBrand, DoorType, DoorBrand, LiftType, ControllerBrand, Cabin, Type, Make, Unit, Item,Complaint, Employee
from .serializers import LiftSerializer, FloorIDSerializer, BrandSerializer, MachineTypeSerializer, MachineBrandSerializer, DoorTypeSerializer, DoorBrandSerializer, LiftTypeSerializer, ControllerBrandSerializer, CabinSerializer, TypeSerializer, MakeSerializer, UnitSerializer, ItemSerializer, UserRegistrationSerializer, UserLoginSerializer,ComplaintSerializer, EmployeeSerializer
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        print(username, password, user)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################ Lift ######################################

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_floor_id(request):
    serializer = FloorIDSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_brand(request):
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_machine_type(request):
    serializer = MachineTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_machine_brand(request):
    serializer = MachineBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_door_type(request):
    serializer = DoorTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_door_brand(request):
    serializer = DoorBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lift_type(request):
    serializer = LiftTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_controller_brand(request):
    serializer = ControllerBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cabin(request):
    serializer = CabinSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


############################ Items ######################################


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_type(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_make(request):
    serializer = MakeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_unit(request):
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=items_export.xlsx'
    response.write(output.read())

    return response


####################################complaints########################################
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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