from django.contrib import admin
from Aplicaciones.User.models import *

# Register your models here.
#Proveedor
class UserAdmin(admin.ModelAdmin):
    list_display = ( "id"),
    search_fields = ("id", "id")
admin.site.register(User,UserAdmin)