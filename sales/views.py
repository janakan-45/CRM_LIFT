from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Route, Branch, ProvinceState, Quotation,Invoice
from .serializers import CustomerSerializer, RouteSerializer, BranchSerializer, ProvinceStateSerializer, QuotationSerializer,InvoiceSerializer
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO


###########################################Customer  views######################################### 
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
            "reference_id": customer.reference_id,
            "site_id": customer.site_id
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
        customer = serializer.save()
        return Response({
            "message": "Customer updated successfully!",
            "reference_id": customer.reference_id,
            "site_id": customer.site_id
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
        'Reference ID', 'Site ID', 'Site Name', 'Contact Person Name', 'Email', 'Site Address',
        'Route', 'Branch', 'Province/State', 'Sector'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    customers = Customer.objects.all()

    for row_num, customer in enumerate(customers, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = customer.reference_id
        ws[f"{get_column_letter(2)}{row_num}"] = customer.site_id
        ws[f"{get_column_letter(3)}{row_num}"] = customer.site_name
        ws[f"{get_column_letter(4)}{row_num}"] = customer.contact_person_name
        ws[f"{get_column_letter(5)}{row_num}"] = customer.email
        ws[f"{get_column_letter(6)}{row_num}"] = customer.site_address
        ws[f"{get_column_letter(7)}{row_num}"] = customer.routes.value if customer.routes else ''
        ws[f"{get_column_letter(8)}{row_num}"] = customer.branch.value if customer.branch else ''
        ws[f"{get_column_letter(9)}{row_num}"] = customer.province_state.value if customer.province_state else ''
        ws[f"{get_column_letter(10)}{row_num}"] = customer.sector

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=customers_export.xlsx'
    response.write(output.read())

    return response


###########################################quotation###################################3



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_quotation(request):
    serializer = QuotationSerializer(data=request.data)
    if serializer.is_valid():
        quotation = serializer.save()
        return Response({
            "message": "Quotation added successfully!",
            "quotation_id": quotation.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_quotation(request, pk):
    try:
        quotation = Quotation.objects.get(pk=pk)
    except Quotation.DoesNotExist:
        return Response({"error": "Quotation not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuotationSerializer(quotation, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Quotation updated successfully!",
            "quotation_id": quotation.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_quotation(request, pk):
    try:
        quotation = Quotation.objects.get(pk=pk)
        quotation.delete()
        return Response({"message": "Quotation deleted successfully!"}, status=status.HTTP_200_OK)
    except Quotation.DoesNotExist:
        return Response({"error": "Quotation not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quotation_list(request):
    quotations = Quotation.objects.all()
    serializer = QuotationSerializer(quotations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_quotations_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Quotations"

    headers = [
        'Reference ID', 'Customer', 'AMC Type', 'Sales/Service Executive', 'Type',
        'Year of Make', 'Date', 'Remark', 'Other Remark'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    quotations = Quotation.objects.all()

    for row_num, quotation in enumerate(quotations, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = quotation.reference_id
        ws[f"{get_column_letter(2)}{row_num}"] = quotation.customer.name if quotation.customer else ''
        ws[f"{get_column_letter(3)}{row_num}"] = quotation.amc_type.name if quotation.amc_type else ''
        ws[f"{get_column_letter(4)}{row_num}"] = quotation.sales_service_executive.name if quotation.sales_service_executive else ''
        ws[f"{get_column_letter(5)}{row_num}"] = quotation.type
        ws[f"{get_column_letter(6)}{row_num}"] = quotation.year_of_make
        ws[f"{get_column_letter(7)}{row_num}"] = quotation.date.strftime('%Y-%m-%d')
        ws[f"{get_column_letter(8)}{row_num}"] = quotation.remark
        ws[f"{get_column_letter(9)}{row_num}"] = quotation.other_remark

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=quotations_export.xlsx'
    response.write(output.read())

    return response




############################invoice views#########################################



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_invoice(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        invoice = serializer.save()
        return Response({
            "message": "Invoice added successfully!",
            "reference_id": invoice.reference_id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_invoice(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Invoice updated successfully!",
            "reference_id": invoice.reference_id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_invoice(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
        invoice.delete()
        return Response({"message": "Invoice deleted successfully!"}, status=status.HTTP_200_OK)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_list(request):
    invoices = Invoice.objects.all()
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_invoices_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"

    headers = [
        'Reference ID', 'Customer', 'AMC Type', 'Start Date', 'Due Date',
        'Discount', 'Payment Term', 'Status'
    ]

    for col_num, header in enumerate(headers, 1):
        ws[f"{get_column_letter(col_num)}1"] = header

    invoices = Invoice.objects.all()

    for row_num, invoice in enumerate(invoices, 2):
        ws[f"{get_column_letter(1)}{row_num}"] = invoice.reference_id
        ws[f"{get_column_letter(2)}{row_num}"] = invoice.customer_name if invoice.customer_name else ''
        ws[f"{get_column_letter(3)}{row_num}"] = invoice.amc_type_name if invoice.amc_type_name else ''
        ws[f"{get_column_letter(4)}{row_num}"] = invoice.start_date.strftime('%Y-%m-%d')
        ws[f"{get_column_letter(5)}{row_num}"] = invoice.due_date.strftime('%Y-%m-%d')
        ws[f"{get_column_letter(6)}{row_num}"] = str(invoice.discount)
        ws[f"{get_column_letter(7)}{row_num}"] = invoice.payment_term
        ws[f"{get_column_letter(8)}{row_num}"] = invoice.status

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=invoices_export.xlsx'
    response.write(output.read())

    return response