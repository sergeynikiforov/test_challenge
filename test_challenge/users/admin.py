from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Team
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'first_name', 'last_name',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Team', {'fields': ('team',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
    search_fields = ('email', 'fist_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


class UserInline(admin.StackedInline):
    model = User
    fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('email', 'first_name', 'last_name')
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    inlines = [
        UserInline,
    ]


# Register the new UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
