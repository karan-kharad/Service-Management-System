from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import *
from api.serializers import RepairJobSerializer,CustomerSerializer,CustomUserSerializer,JobInfoSerializer,CreateRepairJobSerializer

# Create your views here.

class JobListView(generics.ListAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer

class CreateJobView(generics.CreateAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = CreateRepairJobSerializer


class UserJobListView(generics.ListAPIView):
   serializer_class = RepairJobSerializer
   permission_classes = [IsAuthenticated]

   def get_queryset(self):
       return RepairJob.objects.filter(created_by= self.request.user)
    
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class JobDetilsView(generics.RetrieveAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class JobInfo(APIView):
    def get(slef,request):
        jobs = RepairJob.objects.all()
        serializers = JobInfoSerializer({
            'jobs': jobs,
            'jobs_count': jobs.count(),
        })
        return Response(serializers.data)        

