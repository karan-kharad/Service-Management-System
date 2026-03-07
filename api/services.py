from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from .models import Otp
from .utils import generate_otp, hash_otp, varify_otp
from django.core.mail import send_mail
from django.conf import settings

def create_registration_otp(reapir_job):
    row_otp = generate_otp()
    hashed_otp = hash_otp(row_otp)

    expires_at = timezone.now() +timedelta(minutes=5)

    Otp.objects.update_or_create(
        reapir_job = reapir_job,
        otp_type ="REGISTRATION",
        defaults={
            "otp": hashed_otp,
            "expires_at" : expires_at,
            "verified" : False,
            "attempts" : 0,
        },
    )
    return row_otp

def create_delivery_otp(reapir_job):
    raw_otp = generate_otp()
    hashed_otp = (raw_otp)

    expires_at = timezone.now() + timedelta(days=7)

    Otp.objects.update_or_create(
        reapir_job=reapir_job,
        otp_type ="DELIVERY",
        defaults={
            "otp": hashed_otp,
            "expires_at" : expires_at,
            "verified" : False,
            "attempts" : 0,
        },
    )
    return raw_otp



def send_otp_email(email,otp):

    subject = "Your OTP for Device Repair Registration"

    message = f"Hello,\n\nYour OTP for registering your device repair job is: {otp}\n\nThis OTP is valid for 5 minutes.\n\nThank you for using our service!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
)