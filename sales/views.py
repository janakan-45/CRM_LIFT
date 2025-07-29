from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Route, Branch, ProvinceState
from .serializers import CustomerSerializer, RouteSerializer, BranchSerializer, ProvinceStateSerializer
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO

# Dynamic dropdown views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_route(request):
    serializer = RouteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_branch(request):
    serializer = BranchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_province_state(request):
    serializer = ProvinceStateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_routes(request):
    routes = Route.objects.all()
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branches(request):
    branches = Branch.objects.all()
    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_province_states(request):
    province_states = ProvinceState.objects.all()
    serializer = ProvinceStateSerializer(province_states, many=True)
    return Response(serializer.data)

# Customer CRUD views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        return Response({
            "message": "Customer added successfully!",
            "reference_id": customer.reference_id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Customer updated successfully!",
            "reference_id": customer.reference_id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response({"message": "Customer deleted successfully!"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_list(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_customers_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Customers"

    headers = [
        'Reference ID', 'Site Name', 'Contact Person Name', 'Email', 'Site Address',
        'Route', 'Branch', 'Province/State', 'Sector'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    customers = Customer.objects.all()

    for row_num, customer in enumerate(customers, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = customer.reference_id
        ws[f"{get_column_letter(2)}{row_num}"] = customer.site_name
        ws[f"{get_column_letter(3)}{row_num}"] = customer.contact_person_name
        ws[f"{get_column_letter(4)}{row_num}"] = customer.email
        ws[f"{get_column_letter(5)}{row_num}"] = customer.site_address
        ws[f"{get_column_letter(6)}{row_num}"] = customer.routes.value if customer.routes else ''
        ws[f"{get_column_letter(7)}{row_num}"] = customer.branch.value if customer.branch else ''
        ws[f"{get_column_letter(8)}{row_num}"] = customer.province_state.value if customer.province_state else ''
        ws[f"{get_column_letter(9)}{row_num}"] = customer.sector

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=customers_export.xlsx'
    response.write(output.read())

    return response