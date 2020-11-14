# 改文件是自定义模板标签，直接在前端页面传入数据，不用通过views代码，不用修改views代码
from django import template
from comment.forms import CommentForm
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType

register = template.Library()


# 获取评论


@register.simple_tag()
def get_comment_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=ct, object_id=obj.id).count()


@register.simple_tag()
def get_comment_form(obj):
    ct = ContentType.objects.get_for_model(obj)
    form = CommentForm(
        initial={'object_id': obj.id, 'content_type': ct.model, 'reply_comment_id': 0})  # 初始化一个CommentForm表返回给前端页面,并且给object_id，
    return form


@register.simple_tag()
def get_comment_list(obj):
    ct = ContentType.objects.get_for_model(obj)
    blog_comment_list = Comment.objects.filter(content_type=ct, object_id=obj.id, parent=None)  # 获取评论列表
    return blog_comment_list
