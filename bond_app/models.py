from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.conf import settings


#extend User class using AbstractUser
class NewUser(AbstractUser):
    new_field = models.CharField(max_length=100)

    def __str__(self):
        return self.username


def validate_min_len(value):
    if len(value) < 3:
        raise ValidationError(
            ('%(value)s is less than minimum allowed value'),
            params={'value': value},
        )


def validate_value_range(value):
    if value > 100000000:
        raise ValidationError(
            ('%(value)s is greater than maximum allowed value'),
            params={'value': value},
        )
    elif value < 0:
        raise ValidationError(
            ('%(value)s is less than minimum allowed value'),
            params={'value': value},
        )


#create a validator integer with an inclusive range of 1 to 10,000
def validate_value(value):
    
    if value > 10000 or value < 1:
        raise ValidationError(
            ('%(value)s is not allowed. Please enter with an inclusive range of 1 to 10,000'),
            params={'value': value},
        )
   

# Create your models here.
class Bond(models.Model):
    is_cleaned = False
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100,validators=[validate_min_len])
    price = models.DecimalField(max_digits=15, decimal_places=4,validators=[validate_value_range])
    number_of_bond = models.IntegerField(validators=[validate_value])
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer', null=True, blank=True)

    def clean(self):
        self.is_cleaned = True
        if len(self.name) < 3:
            raise ValidationError("Please enter a valid values")
        super(Bond, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(Bond, self).save(*args, **kwargs)