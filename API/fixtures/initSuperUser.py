import os
from clients_api.models import UserClient

def create_super_user():
    mail=os.environ.get("SUPER_USER_MAIL", "admin")
    name=os.environ.get("SUPER_USER_NAME", "admin")
    last_name=os.environ.get("SUPER_USER_LASTNAME", "admin")
    password= os.environ.get("SUPER_USER_PASSWORD","admin")
    pin= os.environ.get("SUPER_USER_PASSWORD","1234")
    UserClient.objects.create_superuser()