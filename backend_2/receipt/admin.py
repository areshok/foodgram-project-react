from django.contrib import admin

from .models import Tag, Ingredient, Receipt

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Receipt)
