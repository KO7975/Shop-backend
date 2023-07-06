from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    model = User
    # add_form = UserCreationForm
    # form = UserChangeForm
    list_display = [
        "email",
        "first_name",
        "last_name",
        "updated_at",
        "is_staff",
        "is_active"
        ]
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Custom Fields",
            {
                'fields': ( 
                    'first_name', 
                    'last_name', 
                    'phone',
                    "gender", 
                    'date_of_birth',
                    'picture',
                )
            }
        )
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Custom Fields",
            {
                'fields': (  
                    'phone',
                    "gender", 
                    'date_of_birth',
                    'picture',
                )
            }
        )        
    )


admin.site.register(User, UserAdmin)
