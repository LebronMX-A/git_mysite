from django.contrib import admin
from likes.models import LikeRecord,LikeCount
from django.contrib.auth.models import User
# Register your models here.


@admin.register(LikeRecord)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id')



@admin.register(LikeCount)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id')