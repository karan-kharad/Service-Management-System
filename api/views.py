from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import *
from api.serializers import RepairJobSerializer,CustomerSerializer,CustomUserSerializer,JobInfoSerializer

# Create your views here.

class JobListView(generics.ListCreateAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer


class UserJobListView(generics.ListCreateAPIView):
   serializer_class = RepairJobSerializer
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
       return RepairJob.objects.filter(created_by= self.request.user)
    
class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# @api_view(['GET'])
# def customer_list(request):
#     customers = Customer.objects.all()
#     serializers = CustomerSerializer(customers, many = True)
#     return Response(serializers.data)


class JobDetilsView(generics.RetrieveAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class JobInfoView(generics.ListCreateAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = JobInfoSerializer

# @api_view(['GET'])
# def jobinfo(request):
#     jobs = RepairJob.objects.all()
#     serializers = JobInfoSerializer({
#         'jobs': jobs,
#         'jobs_count': jobs.count(),
#     })
#     return Response(serializers.data)