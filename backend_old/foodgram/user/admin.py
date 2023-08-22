from django.contrib import admin

# Register your models here.
from .models import User, Follow

admin.site.register(User)
admin.site.register(Follow)

