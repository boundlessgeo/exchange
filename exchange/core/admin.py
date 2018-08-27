from django.contrib import admin
from .models import ExchangeProfile


class ExchangeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_creator', 'content_manager',)


admin.site.register(ExchangeProfile, ExchangeProfileAdmin)
