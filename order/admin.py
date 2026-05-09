from django.contrib import admin
from .models import Oda

@admin.register(Oda)
class OdaAdmin(admin.ModelAdmin):
    list_display = ('id', 'meza', 'chakula', 'status', 'muda') 
    list_filter = ('status',) 