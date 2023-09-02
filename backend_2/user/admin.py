from django.contrib import admin

# Register your models here.
from .models import Subscription, User

admin.site.register(Subscription)
admin.site.register(User)