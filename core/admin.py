from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models

class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['email','first_name','last_name',]
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (_('Personal Info'), {'fields': ('first_name','last_name',)}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1','password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Personnel)
admin.site.register(models.CustomerPhoneNo)
admin.site.register(models.PersonnelPhoneNo)
admin.site.register(models.Branch)
admin.site.register(models.Food)