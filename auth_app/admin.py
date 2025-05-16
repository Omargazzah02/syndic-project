from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserLoginHistory, UserLoginPrediction

# Customize CustomUser admin display
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role',  'residence')
    list_filter = ('role', 'is_active', 'residence')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)


# Login history admin
@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username',)

# Login prediction admin
@admin.register(UserLoginPrediction)
class UserLoginPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_day', 'updated_at')
    list_filter = ('predicted_day',)
    search_fields = ('user__username',)
