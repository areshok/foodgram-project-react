from django.contrib import admin

from .models import Tag, Ingredient, Receipt, TagReceipt, IngredientReceipt, FavoritesReceipt, ShoppingList

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Receipt)
admin.site.register(TagReceipt)
admin.site.register(IngredientReceipt)
admin.site.register(FavoritesReceipt)
admin.site.register(ShoppingList)
