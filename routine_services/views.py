from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from io import StringIO, BytesIO
import csv
import logging

from .models import RoutineService
from authentication.models import CustomUser  # ✅ Import CustomUser
from .serializers import RoutineServiceSerializer

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

logger = logging.getLogger(__name__)

# =====================
# CRUD for RoutineService
# =====================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_routine_services(request):
    services = RoutineService.objects.all().select_related('lift', 'customer', 'employee', 'route')
    serializer = RoutineServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_routine_service(request):
    serializer = RoutineServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_routine_service(request, pk):
    service = get_object_or_404(RoutineService, pk=pk)
    serializer = RoutineServiceSerializer(service)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_routine_service(request, pk):
    service = get_object_or_404(RoutineService, pk=pk)
    serializer = RoutineServiceSerializer(service, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_routine_service(request, pk):
    service = get_object_or_404(RoutineService, pk=pk)
    service.delete()
    return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# =====================
# Export to CSV
# =====================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_routine_services_to_csv(request):
    output = StringIO()
    writer = csv.writer(output)

    headers = [
        'Customer Reference No', 'Lift Code', 'Service Date', 'Customer Name',
        'Customer Location', 'Employee Name', 'Route Name', 'No. of Services', 'Status'
    ]
    writer.writerow(headers)

    routine_services = RoutineService.objects.all().select_related('customer', 'employee', 'route')

    for service in routine_services:
        writer.writerow([
            service.customer_ref,
            service.lift_code,
            service.service_date.strftime('%Y-%m-%d %H:%M:%S') if service.service_date else '',
            service.customer.site_name if service.customer else '',
            service.customer.site_address if service.customer and hasattr(service.customer, 'site_address') else '',
            service.employee.username if service.employee else '',  # ✅ now using CustomUser
            service.route.route_name if service.route else '',
            service.no_of_services,
            service.status
        ])

    output.seek(0)
    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=routine_services_export.csv'
    return response


# =====================
# Print Routine Service (PDF)
# =====================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def print_routine_service(request, pk):
    try:
        routine_service = get_object_or_404(RoutineService, pk=pk)

        context = {
            'company_name': 'Atom Lifts India Pvt Ltd',
            'address': 'No.87B, Pillayar Koll Street, Mannurpet, Ambattur Indus Estate, Chennai 50, CHENNAI',
            'phone': '9600087456',
            'email': 'admin@atomlifts.com',
            'service_ref': routine_service.customer_ref,
            'service_date': routine_service.service_date.strftime('%d/%m/%Y %H:%M:%S') if routine_service.service_date else '',
            'lift_code': routine_service.lift_code,
            'customer_name': routine_service.customer.site_name if routine_service.customer else '',
            'customer_location': routine_service.customer.site_address if routine_service.customer and hasattr(routine_service.customer, 'site_address') else '',
            'employee_name': routine_service.employee.username if routine_service.employee else '',  # ✅ CustomUser
            'employee_role': routine_service.employee.role if routine_service.employee else '',      # ✅ Show role
            'route_name': routine_service.route.route_name if routine_service.route else '',
            'no_of_services': routine_service.no_of_services,
            'status': routine_service.status
        }

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        story = []

        header_style = ParagraphStyle(
            name='HeaderStyle',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1
        )
        story.append(Paragraph(context['company_name'], header_style))
        story.append(Paragraph(context['address'], styles['Normal']))
        story.append(Paragraph(f"Phone: {context['phone']} | Email: {context['email']}", styles['Normal']))
        story.append(Spacer(1, 12))

        data = [
            ['Service Reference:', context['service_ref']],
            ['Date:', context['service_date']],
            ['Lift Code:', context['lift_code']],
            ['Status:', context['status']],
        ]
        table = Table(data, colWidths=[100, 400])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        story.append(Paragraph("Customer Details", styles['Heading2']))
        data = [
            ['Customer Name:', context['customer_name']],
            ['Customer Location:', context['customer_location']],
        ]
        table = Table(data)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        story.append(Paragraph("Service Details", styles['Heading2']))
        story.append(Paragraph(f"Employee: {context['employee_name']} ({context['employee_role']})", styles['Normal']))
        story.append(Paragraph(f"Route: {context['route_name']}", styles['Normal']))
        story.append(Paragraph(f"No. of Services: {context['no_of_services']}", styles['Normal']))
        story.append(Spacer(1, 12))

        doc.build(story)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=routine_service_{context["service_ref"]}.pdf'
        return response

    except Exception as e:
        logger.error(f"Unexpected error in print_routine_service: {str(e)}")
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
