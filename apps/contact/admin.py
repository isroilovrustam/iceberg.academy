from django.contrib import admin
from .models import Contact, About, Goal
from .translations import CustomTranslationsAdmin


@admin.register(Contact)
class Admin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_view', 'create_date']
    list_filter = ['is_view']

@admin.register(Goal)
class Admin(CustomTranslationsAdmin):
    list_display = ['title']

@admin.register(About)
class Admin(CustomTranslationsAdmin):
    list_display = ['title']
