from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class LikeCount(models.Model):
    # 这三个是描述ContentType的
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 已点赞数量
    liked_num = models.IntegerField(default=0)


# 具体的点赞记录
class LikeRecord(models.Model):
    # 对 哪个对象 进行点赞
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 谁点赞
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 点赞时间
    liked_time = models.DateTimeField(auto_now_add=True)