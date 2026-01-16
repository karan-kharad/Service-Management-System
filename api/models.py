from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class Customer(models.Model):
   customer_name = models.CharField(max_length= 255, blank=True, null=True)
   customer_phone = models.CharField(max_length=13, blank=True, null=True)
   customer_email = models.EmailField(blank=True, null=True)
   address = models.TextField(blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
    
class RepairJob(models.Model):
    #id = models.UUIDField(primary_key=True)
    customer = models.ForeignKey(Customer,related_name='repair_jobs', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=13, blank=True, null=True)
    address = models.TextField()
    device_type = models.CharField(max_length=100, blank=True, null=True)
    device_brand = models.CharField(max_length=100, blank=True, null=True)
    device_model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    device_image = models.ImageField(upload_to='device_images/', blank=True, null=True)
    problem_description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending')
    assigned_engineer = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
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
    

    
