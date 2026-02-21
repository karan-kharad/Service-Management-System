from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from datetime import *
# Create your models here.
class CustomUser(AbstractUser):
    ROLES_CHOICES = [
        ("admin","admin"),
        ("owner","owner"),
        ("engineer","engineer"),
        ]
    
    role = models.CharField(max_length=150, choices=ROLES_CHOICES, default='engineer')
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='admin', on_delete=models.CASCADE)
    admin_key = models.CharField(max_length=50,blank=True,null=True)

class OnwerProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name="owner", on_delete=models.CASCADE)
    shop_licenes_no =models.CharField(max_length=50,blank=True,null=True)
    shop_name = models.CharField(max_length=150)

class EngineerProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='engineer', on_delete=models.CASCADE)
    onwer = models.ForeignKey(OnwerProfile, on_delete=models.CASCADE)
    employer_id = models.CharField(max_length=50,unique=True)
class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=13, unique=True)
    customer_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.customer_name} - {self.customer_phone}"
       
class RepairJob(models.Model):
    STATUS_CHOICES = [
    ("COLLECTED", "Collected"),
    ("DIAGNOSING", "Diagnosing"),
    ("REPAIRING", "Repairing"),
    ("READY", "Ready for Delivery"),
    ("DELIVERED", "Delivered"),
]
    customer = models.ForeignKey(Customer,related_name='repair_jobs',on_delete=models.PROTECT)
    device_type = models.CharField(max_length=100, blank=True, null=True)
    device_brand = models.CharField(max_length=100, blank=True, null=True)
    device_model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    device_image = models.ImageField(upload_to='device_images/', blank=True, null=True)
    problem_description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="COLLECTED", max_length=20)
    assigned_engineer = models.ForeignKey(CustomUser, related_name='jobs', blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(CustomUser, related_name='created_jobs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RepairJob {self.id} - {self.device_type} for {self.customer_name}"

class ReplacedParts(models.Model):
    repair_jab = models.ForeignKey(RepairJob,related_name='replaced_parts', on_delete=models.CASCADE)
    part_name = models.CharField(max_length=225)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    repaled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part_name} for RepairJob {self.repair_job.id}"
    
class Otp(models.Model):
    OTP_TYPE_CHOCIE = [
         ("REGISTRATION", "Registration"),
        ("DELIVERY", "Delivery"),
    ]

    reapir_job = models.ForeignKey(RepairJob,
        on_delete=models.CASCADE,
        related_name='otp'
    )

    otp_type = models.CharField(max_length=28,choices=OTP_TYPE_CHOCIE)
    otp = models.CharField(max_length=128)
    attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_locked(self):
        return self.locked_until and timezone.now() < self.locked_until