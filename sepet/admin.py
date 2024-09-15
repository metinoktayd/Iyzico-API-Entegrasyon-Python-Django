from django.contrib import admin
from .models import Urun
# Register your models here.

class UrunAdmin(admin.ModelAdmin):
    list_display = ['ad']
    search_fields = ['ad']

admin.site.register(Urun, UrunAdmin)
