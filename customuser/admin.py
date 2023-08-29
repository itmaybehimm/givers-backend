from dataclasses import field
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import PermissionsMixin

from .models import User

# Register your models here.
admin.site.register(User)
# and since we are not using Django's build-in permissions,
# Unregister the Group model from admin
# admin.site.unregister(Group)
