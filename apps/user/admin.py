from django.contrib import admin
from .models import User, Team, VerifyPhone
from .translation import CustomTranslationsAdmin


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    list_display_links = ['phone']
    fields = ['name', 'phone', 'image']


@admin.register(Team)
class Admin(CustomTranslationsAdmin):
    list_display = ['profession', 'name']


@admin.register(VerifyPhone)
class Admin(admin.ModelAdmin):
    list_display = ['phone', 'code']
