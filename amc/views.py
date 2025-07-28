from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AMC, AMCType, PaymentTerms,Customer
from .serializers import AMCSerializer, AMCTypeSerializer, PaymentTermsSerializer,CustomerSerializer
from django.core.exceptions import ValidationError

@api_view(['POST'])
def add_amc_type(request):
    serializer = AMCTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_payment_terms(request):
    serializer = PaymentTermsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_amc_types(request):
    amc_types = AMCType.objects.all()
    serializer = AMCTypeSerializer(amc_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_payment_terms(request):
    payment_terms = PaymentTerms.objects.all()
    serializer = PaymentTermsSerializer(payment_terms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_amc(request):
    serializer = AMCSerializer(data=request.data)
    if serializer.is_valid():
        amc = serializer.save()
        return Response({
            "message": "AMC added successfully!",
            "reference_id": amc.reference_id,
            "customer_id": amc.customer.customer_id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_amc(request, pk):
    try:
        amc = AMC.objects.get(pk=pk)
    except AMC.DoesNotExist:
        return Response({"error": "AMC not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AMCSerializer(amc, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "AMC updated successfully!",
            "reference_id": amc.reference_id,
            "customer_id": amc.customer.customer_id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_amc(request, pk):
    try:
        amc = AMC.objects.get(pk=pk)
        amc.delete()
        return Response({"message": "AMC deleted successfully!"}, status=status.HTTP_200_OK)
    except AMC.DoesNotExist:
        return Response({"error": "AMC not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def amc_list(request):
    amcs = AMC.objects.all()
    serializer = AMCSerializer(amcs, many=True)
    return Response(serializer.data)