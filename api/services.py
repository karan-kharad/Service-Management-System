from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from .models import Otp
from .utils import generate_otp, hash_otp, varify_otp

def create_registration_otp(repair_job):
    row_otp = generate_otp()
    hashed_otp = hash_otp(row_otp)

    expire_at = timezone.now() +timedelta(min=5)

    Otp.objects.update_or_create(
        repair_job = repair_job,
        otp_type ="REGISTRATION",
        defaults={
            "otp": hashed_otp,
            "expires_at" : expire_at,
            "verified" : False,
            "attempts" : 0,
        },
    )
    return row_otp

def create_delivery_otp(repair_job):
    raw_otp = generate_otp()
    hashed_otp = (raw_otp)

    expires_at = timezone.now() + timedelta(days=7)

    Otp.objects.update_or_create(
        repair_job=repair_job,
        otp_type ="DELIVERY",
        defaults={
            "otp": hashed_otp,
            "expires_at" : expires_at,
            "verified" : False,
            "attempts" : 0,
        },
    )
    return raw_otp