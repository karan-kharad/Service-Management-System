from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import *
from api.serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAdminUser
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):

    def post(self,request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password']
         )
        if not user:
                return Response(
                    {"message":"Invaid certionsal"}, status=status.HTTP_400_BAD_REQUEST
                    )

        refresh = RefreshToken.for_user(user)

        return Response({
                "access_token" : str(refresh.access_token),
                "refresh_token" : str(refresh),
                "role":user.role,
                "user":user.username
                }, status=status.HTTP_200_OK)

class JobListView(generics.ListAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer

# this for posting the job
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

class JobDetilsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE'] :
            self.permission_classes=[IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

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