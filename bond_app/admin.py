from django.contrib import admin

# Register your models here.
from .models import NewUser, Bond

admin.site.register(NewUser)
admin.site.register(Bond)