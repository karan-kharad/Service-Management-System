from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from api.serializers import RepairJobSerializer,CustomerSerializer,CustomUserSerializer

# Create your views here.

def job_list(request):
    job = RepairJob.objects.all()
    serializers = RepairJobSerializer(job, many=True)
    return JsonResponse(
        {
            'data':serializers.data
        }
    )

@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.all()
    serializers = CustomerSerializer(customers, many = True)
    return Response(serializers.data)
@api_view(['GET'])

def job_detils(request, pk):
    job = get_object_or_404(RepairJob,pk=pk)
    serializers = RepairJobSerializer(job)
    return Response(serializers.data)

@api_view(['GET'])
def user_list(request):
    user = CustomUser.objects.all()
    serializers = CustomUserSerializer(user, many=True)
    return Response(serializers.data)