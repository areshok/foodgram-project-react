from django.contrib import admin

from .models import Tag, Ingredient, Receipt, TagReceipt, IngredientReceipt, FavoritesReceipt

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Receipt)
admin.site.register(TagReceipt)
admin.site.register(IngredientReceipt)
admin.site.register(FavoritesReceipt)