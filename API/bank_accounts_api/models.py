from datetime import datetime, timedelta
from random import choice
from django.db import models
from utils.encryption import Encrypter
from utils.ccgen import gen_card
from cryptography.fernet import Fernet
from django.conf import settings

# class CardManaget(models.Manager):
#     def create_card

class Card(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=255)
    register_date = models.DateTimeField(auto_now=True)
    expiration_date = models.CharField(max_length=255)
    ccv = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50,unique=True, blank=False, null=False)
    pin = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    last_digits=models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)

    def encrypt_pin(self,pin,salt):
        encryp=Encrypter(settings.ENCRYPT_KEY,salt)
        token = encryp.encrypt_data(pin)
        return token

    def decrypt_pin(self,token=None):
        encryp=Encrypter(settings.ENCRYPT_KEY,salt=self.salt)
        pin = encryp.decrypt_data(str(self.pin))
        return pin['data']

    def reset_pin(self,pin):
        old_pin=self.decrypt_pin(token=self.pin,salt=self.salt)
        self.pin=self.encrypt_pin(pin=pin,salt=self.salt)
        return True

    @classmethod
    def create(cls, client, pin, is_staff):
        if is_staff == False:
            encryp=Encrypter(pin)
            card = cls(client=client)
            card.salt=encryp.salt_text()
            card.pin = cls.encrypt_pin(cls,pin=pin,salt=card.salt)
            new_card = str(gen_card())
            card.card_number = encryp.encrypt_data(new_card)
            card.expiration_date = encryp.encrypt_data(datetime.now() + timedelta(weeks = 144))
            card.ccv = encryp.encrypt_data(choice(list(range(100,1000))))
            card.account_number = cls.acount_number_validator(cls)
            last_digits = new_card[-4:]
            card.last_digits = last_digits
            card.save()
            return card

    def acount_number_validator(self):
        num = int("2101"+str(choice(range(1000,10000)))+str(choice(range(1000,10000))))
        if self.objects.filter(account_number=num).exists():
            self.acount_number_validator()
        else:
            return str(num)

    def decrypt_data(self,pin):
        encryp=Encrypter(pin,self.salt)
        cn=encryp.decrypt_data(self.card_number)['data']
        ccv=encryp.decrypt_data(self.ccv)['data']
        date=encryp.decrypt_data(self.expiration_date)['data']
        return {"card_number":cn,"ccv":ccv,"expiration_date":date}

    def get_expense_operations(self):
        return self.operation_sender.all()

    def get_income_operations(self):
        return self.operation_receiver.all()

    def get_all_operations(self):
        return self.get_income_operations() | self.get_expense_operations()
    
    def get_balance(self):
        expense=0.0
        income=0.0
        print(self.get_expense_operations())
        print("holaaaa\n\n\n")
        for operation in self.get_income_operations():
            income += float(operation.amount)
        for operation in self.get_expense_operations():
            expense += float(operation.amount)
        balance = income-expense
        return balance

    def __str__(self):
        return f"{self.client.name} {self.client.last_name}:{self.account_number}"
class Operation(models.Model):
    datetime = models.DateTimeField(blank=False, null=False, auto_now=True)
    description = models.CharField(max_length=80, blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    egreso = models.BooleanField()
    sender_card = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name="operation_sender")
    receiving_card = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name="operation_receiver")