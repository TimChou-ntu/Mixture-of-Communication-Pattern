from django.contrib import admin
from rest_framework.permissions import OR
from .models import FibReqItem, FibResItem

# Register your models here.

admin.site.register(FibReqItem)
admin.site.register(FibResItem)