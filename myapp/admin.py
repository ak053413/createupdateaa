from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'bio', 'propic']
