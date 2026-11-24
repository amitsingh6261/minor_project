
from django.contrib import admin
from .models import UserProfile, Group, Message


# User Profile Admin

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'date_of_birth', 'created_at')

    search_fields = ('user__username', 'user__email')


# Group Admin

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = ('name', 'created_by', 'created_at')

    search_fields = ('name', 'created_by__username')

    filter_horizontal = ('members',)


# Message Admin

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ('sender', 'receiver', 'group', 'created_at')

    search_fields = ('sender__username', 'content')

    list_filter = ('created_at',)
