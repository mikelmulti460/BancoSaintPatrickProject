from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from bank_accounts_api.models import Card
from django.db.models.signals import post_save
from django.conf import settings

class UserClientManager(BaseUserManager):
    """Manager for Users Client"""

    def create_user(self, email, name, last_name, pin, password=None, is_staff = False):
        """Create New User Client"""
        if not email:
            raise ValueError('El usuario debe tener un Email')
        
        email = self.normalize_email(email=email)
        user = self.model(email=email, name=name, last_name=last_name, pin=int(pin))
        user.is_staf=is_staff
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, last_name,  pin, password):
        user = self.create_user(email, name, last_name, pin, password, is_staff=True)
        user.pin=None
        user.is_superuser = True
        user.save(using = self._db)

        return user

class UserClient(AbstractBaseUser, PermissionsMixin):
    """ Model Data Base for Users in the System """
    email = models.EmailField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    pin = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', 'pin']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

#signals
def create_user_card(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"] and user.is_staff == False:
        card = Card()
        card.create(user, user.pin, user.is_staff)
        user.pin=None
        user.save()
post_save.connect(create_user_card, sender=UserClient)