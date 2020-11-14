from django.contrib import admin
from blog.models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','get_read_num','blog_type','author','create_time','last_updata_time')#readnum为ReadNum模型
