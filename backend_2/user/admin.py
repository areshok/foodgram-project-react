from django.contrib import admin

from .models import Subscription, User


class SubscriptionInstanceInline(admin.TabularInline):
    model = Subscription
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    inlines = [SubscriptionInstanceInline]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('author',)
    search_fields = ('user',)


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)