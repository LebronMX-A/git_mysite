from django.contrib import admin
from .models import  Comment
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'object_id', 'text', 'content_time', 'user')