from django.contrib import admin

from .models import (FavoritesReceipt, Ingredient, IngredientReceipt, Receipt,
                     ShoppingList, Tag, TagReceipt)


class IngridientInstanceInline(admin.TabularInline):
    model = IngredientReceipt


class TagInstanceInline(admin.TabularInline):
    model = TagReceipt


class FavoritesReceiptInstanceInline(admin.TabularInline):
    model = FavoritesReceipt


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class ReceiptAdmin(admin.ModelAdmin):
    model = Receipt
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'author', 'tags',)
    inlines = [IngridientInstanceInline, TagInstanceInline]


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(TagReceipt)
admin.site.register(IngredientReceipt)
admin.site.register(FavoritesReceipt)
admin.site.register(ShoppingList)
