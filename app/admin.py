from django.contrib import admin

# Register your models here.
from .models import Contact as ct

admin.site.register(ct)