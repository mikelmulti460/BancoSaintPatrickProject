import os
from clients_api.models import UserClient
from bank_accounts_api.models import Card
from django.db.utils import IntegrityError
def create_super_user():
    email=os.environ.get("SUPER_USER_MAIL", "admin")
    name=os.environ.get("SUPER_USER_NAME", "admin")
    last_name=os.environ.get("SUPER_USER_LASTNAME", "admin")
    password= os.environ.get("SUPER_USER_PASSWORD","admin")
    pin= os.environ.get("SUPER_USER_PIN","1234")
    user=UserClient.objects.create_superuser(email,name,last_name,pin,password=password)
    user.is_staff=True
    #if os.environ.get("DEBUG",False):
        #Card.create(user,pin, False)
    user.save()
try:
    create_super_user()
except IntegrityError:
    print("\n Saltando la creación de user usuario: El usuario ya existe!\n")