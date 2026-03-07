import secrets
from django.contrib.auth.hashers import make_password, check_password


def generate_otp():
    return str(secrets.randbelow(900000)+ 100000)

def hash_otp(otp):
    return make_password(otp)

def varify_otp(input_otp,hash_otp):
    return check_password(input_otp,hash_otp)
