from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, PhoneCode


admin.site.register(User, UserAdmin)
admin.site.register(Profile, admin.ModelAdmin)
admin.site.register(PhoneCode, admin.ModelAdmin)
