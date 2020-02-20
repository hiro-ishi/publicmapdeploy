from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Post
from django.contrib.gis.admin import OSMGeoAdmin

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Post)
class PostAdmin(OSMGeoAdmin):
    list_display = ('number', 'location')
