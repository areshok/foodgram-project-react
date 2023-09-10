from django.contrib import admin

from .models import Tag, Ingredient, Receipt, TagReceipt, IngredientReceipt, FavoritesReceipt, ShoppingList


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)




admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Receipt)
admin.site.register(TagReceipt)
admin.site.register(IngredientReceipt)
admin.site.register(FavoritesReceipt)
admin.site.register(ShoppingList)
