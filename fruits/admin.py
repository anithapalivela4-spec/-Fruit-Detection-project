from django.contrib import admin
from .models import Fruit, Variety

@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ('fruit_name', 'scientific_name', 'variety', 'growth_stage', 'created_at')
    search_fields = ('fruit_name', 'scientific_name', 'description')
    list_filter = ('growth_stage', 'created_at')
