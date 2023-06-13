from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm



class UserAdmin(UserAdmin):
    model = User
    # add_form = UserCreationForm
    # form = UserChangeForm
    # list_display = ["id", "email", "updated_at", "is_staff"]
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Custom Fields",
            {
                'fields': ( 
                    'first_name', 
                    'last_name', 
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
                    "gender", 
                    'date_of_birth',
                    'picture',
                )
            }
        )        
    )


admin.site.register(User, UserAdmin)
