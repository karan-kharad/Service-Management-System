from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

0# Create your models here.
class CustomUser(AbstractUser):

    ROLES_CHOICES = [
        ("admin","admin"),
        ("onwer","onwer"),
        ("engineer","engineer"),
        ]
    
    role = models.CharField(max_length=150, choices=ROLES_CHOICES, default='engineer')
    # username = models.CharField(max_length=150, unique=True)
    # email = models.EmailField(unique=True)
    # phone = models.CharField(max_length=13, blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.username

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
    customer_email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    device_type = models.CharField(max_length=100, blank=True, null=True)
    device_brand = models.CharField(max_length=100, blank=True, null=True)
    device_model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    device_image = models.ImageField(upload_to='device_images/', blank=True, null=True)
    problem_description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending')
    assigned_engineer = models.ForeignKey(CustomUser, related_name='jobs', blank=True, null=True, on_delete=models.CASCADE)
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
    phone = models.CharField(max_length=13, blank=True, null=True)
    otp = models.CharField(max_length=6)
    exprie_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    verified = models.BooleanField(default='not verified')
    