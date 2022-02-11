
from datetime import datetime, timedelta
from random import choice
from django.db import models
from utils import ccgen

# class CardManaget(models.Manager):
#     def create_card

class Card(models.Model):
    client = models.ForeignKey("clients_api.UserClient", on_delete=models.CASCADE)
    card_number = models.BigIntegerField(unique=True, blank=False, null=False)
    regiter_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateField(unique=True, blank=False, null=False)
    ccv = models.IntegerField()
    account_number = models.BigIntegerField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    @classmethod
    def create(cls, client):
        card = cls(client=client)
        card.card_number = ccgen.gen_card()
        card.expiration_date = datetime.now() + timedelta(weeks = 144)
        card.csv = choice(list(range(100,1000)))
        card.account_number = int("2101"+str(choice(range(1000,10000)))+str(choice(range(1000,10000))))
        return card


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
    origin_account = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name="origin_account")
    destination_account = models.ForeignKey(Card, on_delete=models.CASCADE, null= False, blank= False, related_name='destination_account')
