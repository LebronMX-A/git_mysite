from django import template
from django.contrib.contenttypes.models import ContentType
from likes.models import LikeCount, LikeRecord

register = template.Library()


@register.simple_tag()
def get_likes_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=obj.pk)
    return like_count.liked_num


@register.simple_tag(takes_context=True)  # 可以获取到所在模板页面所使用的模板变量，比如模板context
def get_likes_status(context, obj):
    ct = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:  # 没有登录也返回没有active
        return ''
    if LikeRecord.objects.filter(content_type=ct, object_id=obj.id, user=user).exists():  # 如果已经点赞了，说明是active
        return 'active'
    else:
        return ''  # 没有记录的话说明没有点赞


@register.simple_tag()
def get_content_type(obj):
    ct = ContentType.objects.get_for_model(obj)
    return ct.model
