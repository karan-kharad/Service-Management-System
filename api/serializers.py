from rest_framework import serializers
from .models import CustomUser,Customer,RepairJob,ReplacedParts,Otp

class RepairJobSerializer(serializers.ModelSerializer):
    class Meta:
       
        model = RepairJob
        fields = (
            'id',
            'customer_name',
            'customer_phone',
            'device_type',
            'device_brand',
            'assigned_engineer',
        )

class CustomUserSerializer(serializers.ModelSerializer):
    jobs = RepairJobSerializer(many = True, read_only = True)
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'phone',
            'is_active',
            'jobs'
        )

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Customer
        fields = (
            'customer_name',
            'customer_phone',
            'customer_email'
        )


class JobInfoSerializer(serializers.Serializer):
    # we get all job, count of jobs, number of parst change
    jobs = RepairJobSerializer(many= True)
    jobs_count = serializers.IntegerField()
