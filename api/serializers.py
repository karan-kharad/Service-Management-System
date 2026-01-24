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



class CreateRepairJobSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField()
    customer_phone = serializers.CharField()
    customer_email = serializers.EmailField()
    address = serializers.CharField()
    class Meta:
       
        model = RepairJob
        fields = (
            'customer_name',
            'customer_phone',
            'address',
            'device_type',
            'customer_email',
            'device_brand',
            'device_model',
            'serial_number',
            'problem_description',
            'status',
            'assigned_engineer',
            'created_by',
            'created_at'
        )

    def create(self,validated_data):
            customer = Customer.objects.create(
                customer_name = validated_data.get('customer_name'),
                customer_phone = validated_data.get('customer_phone'),
                customer_email = validated_data.get('email_name'),
                address = validated_data.get('address'),
            )

            repair_job= RepairJob.objects.create(

                customer = customer,
                customer_name= customer.customer_name ,
                customer_phone= customer.customer_phone ,
                customer_email = customer.customer_email ,
                address=customer.address,
                device_type= validated_data.get('device_type'),
                device_brand=validated_data.get('device_brand'),
                device_model=validated_data.get('device_model'),
                serial_number=validated_data.get('serial_number'),
                problem_description=validated_data.get('problem_description'),
                assigned_engineer=validated_data.get('assigned_engineer'),
                created_by=self.context['request'].user
            )
            return repair_job