from rest_framework import serializers
from .models import *

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
            'eamil',
            'role'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role == 'admin':
            data['Profile'] == AdminProfile.objects.filter(user = instance).values().first()
        elif instance.role == 'onwer':
            data['profile'] == OnwerProfile.objects.filter(user = instance).values().first()
        elif instance.role == 'enginner':
            data['profile'] == EngineerProfile.objects.filter(user = instance).values().first()

        return data

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
        read_only_fields = ('created_by', 'created_at')

    def create(self,validated_data):
            customer = Customer.objects.create(
                customer_name = validated_data.get('customer_name'),
                customer_phone = validated_data.get('customer_phone'),
                customer_email = validated_data.get('customer_email'),
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
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES_CHOICES)
    admin_key = serializers.CharField(required = False, allow_blank = True)
    shop_licenes_no = serializers.CharField( required =False, allow_blank=True)
    shop_name = serializers.CharField(required= False, allow_blank=True)
    employer_id = serializers.CharField(required= False, allow_blank= True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'email',
            'role',
            'admin_key',
            'shop_licenes_no',
            'shop_name',
            'employer_id'
            
        ]

    def validate(self, data):
        role = data.get('role')
        if role == 'admin' and not data.get('admin_key'):
            return serializers.ValidationError({"admin_key" :'admin key required for the admin role'})
        elif role == 'owner' and not data.get('shop_licenes_no','shop_name'):
            return serializers.ValidationError({"shop_licenes_no":'shop licenes is required foe owner role'})
        elif role == 'engineer' and not data.get('employer_id'):
            raise serializers.ValidationError({"employer_id":' employer_id is required foe owner role'})
        return data
       
    def create(self, validated_data):
        role = validated_data.pop('role')
        profile_data={
            'admin_key' : validated_data.pop('admin_key'),
            'shop_licenes_no': validated_data.pop('shop_licenes_no'),
            'employer_id': validated_data.pop('employer_id'),
            'shop_name': validated_data.pop('shop_name')
        }
        user = CustomUser.objects.create_user(**validated_data, role = role)
        if role == 'admin':
            AdminProfile.objects.create(
                user = user,
                admin_key = profile_data['admin_key']
            )
        elif role == 'owner':
            OnwerProfile.objects.create(
                user = user,
                shope_licenes_no = profile_data['shope_lincenes_no']
            )
        elif role == 'enginner':
            EngineerProfile.objects.create(
                user = user,
                employer_id = profile_data['employer_id']
            )
        return user