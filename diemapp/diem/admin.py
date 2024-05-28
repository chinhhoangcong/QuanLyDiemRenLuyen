from django.contrib import  admin
from .models import QuyChe


class QuyCheAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ten', 'diemTong']


admin.site.register(QuyChe, QuyCheAdmin)