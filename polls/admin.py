from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Survey, Question, Choice, CustomUser

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'full_name', 'email', 'role', 'position', 'department', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('full_name', 'position', 'department', 'role'),
        }),
    )