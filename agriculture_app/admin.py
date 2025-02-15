from django.contrib import admin
from .models import ContactMessage, PoultryInventory, EggProduction, DiseaseManagement

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')  
    search_fields = ('name', 'email')  
    list_filter = ('created_at',)  


admin.site.register(PoultryInventory)
admin.site.register(EggProduction)
admin.site.register(DiseaseManagement)