
from datetime import datetime, timedelta
from random import choice
from django.db import models
from utils import ccgen, encryption
from cryptography.fernet import Fernet
from django.conf import settings

# class CardManaget(models.Manager):
#     def create_card

class Card(models.Model):
    client = models.ForeignKey("clients_api.UserClient", on_delete=models.CASCADE)
    card_number = models.BigIntegerField(unique=True, blank=False, null=False, primary_key=True)
    register_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateField(unique=True, blank=False, null=False)
    ccv = models.IntegerField()
    account_number = models.BigIntegerField(unique=True, blank=False, null=False)
    pin = models.IntegerField()
    is_active = models.BooleanField(default=True)

    @classmethod
    def create(cls, client, pin):
        card = cls(client=client, pin=pin)
        card.pin = encryption.encrypt(ccgen.gen_card(),Fernet(settings.ENCRYPT_KEY+str(cls.pin)))
        card.card_number = encryption.encrypt(ccgen.gen_card(),Fernet(settings.ENCRYPT_KEY+str(cls.pin)))
        card.expiration_date = encryption.encrypt(datetime.now() + timedelta(weeks = 144),Fernet(settings.ENCRYPT_KEY+str(cls.pin)))
        card.ccv = encryption.encrypt(choice(list(range(100,1000))),Fernet(settings.ENCRYPT_KEY+str(cls.pin)))
        card.account_number = cls.acount_number_validator(cls)
        card.save()
        return card

    def acount_number_validator(self):
        num = int("2101"+str(choice(range(1000,10000)))+str(choice(range(1000,10000))))
        if self.objects.filter(account_number=num).exists():
            self.acount_number_validator()
        else:
            return num

    def decrypt_data(self,pin):
        cn=encryption.decrypt(self.card_number,Fernet(settings.ENCRYPT_KEY+str(pin)))
        ccv=encryption.decrypt(self.ccv,Fernet(settings.ENCRYPT_KEY+str(pin)))
        date=encryption.decrypt(self.expiration_date,Fernet(settings.ENCRYPT_KEY+str(pin)))
        return {"card_number":cn,"ccv":ccv,"expiration_date":date}

    def get_expense_operations(self):
        return self.operations_set.filter(type="egreso")

    def get_income_operations(self):
        return self.operations_set.filter(type="ingreso")

    def get_all_operations(self):
        return self.operations.all()


class Operations(models.Model):
    datetime = models.DateTimeField(blank=False, null=False)
    description = models.CharField(max_length=80, blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    type = models.CharField(max_length=12, choices=(('ingreso','ingreso'),('egreso','egreso')))
    origin_account = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name="operation_origin")
    destination_account = models.ForeignKey(Card, on_delete=models.CASCADE, null= False, blank= False, related_name='operation_destination')
