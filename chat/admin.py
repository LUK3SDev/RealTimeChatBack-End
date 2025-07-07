from django.contrib import admin
from .models import ChatRoom, ChatRoomMember, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "room_type", "created_at")
    search_fields = ("name", "room_type")

@admin.register(ChatRoomMember)
class ChatRoomMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "chat_room", "joined_at")
    search_fields = ("user__username", "chat_room__name")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat_room", "sender", "key_id", "created_at")
    search_fields = ("chat_room__name", "sender__username", "content")


