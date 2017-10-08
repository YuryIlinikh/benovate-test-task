from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from transfers.models import Inn, Profile


admin.site.register(Inn)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)