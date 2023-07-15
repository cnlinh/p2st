from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_id",
        "email",
        "name",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )


admin.site.register(User, UserAdmin)

# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
