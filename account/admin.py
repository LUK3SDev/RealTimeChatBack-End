from django.contrib import admin
from .models import User, UserPublicKey


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("uuid", "username", "email", "phone_number")
    search_fields = ("uuid", "username", "email", "phone_number")


@admin.register(UserPublicKey)
class UserPublicKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "public_key", "key_id")
    search_fields = ("user__username", "key_id")