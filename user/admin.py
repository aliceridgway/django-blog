from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Profile
from .forms import CustomUserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name','last_name','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','profile_picture','username')}),
        ('Permissions', {'fields': ('is_admin','is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



admin.site.register(User, UserAdmin)
admin.site.register(Profile)

# Groups are not required as we're not using the permissions mixin with our User model
admin.site.unregister(Group)