from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('item_name',)
    list_editable = ('price', 'status') # Admin can edit price/status on the fly