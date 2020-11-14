from datetime import datetime

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone

class ReadNum(models.Model):
    # 统计阅读数量
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)#通过contetentype找到对应的模型
    object_id = models.PositiveIntegerField()#记录对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpend():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetail(models.Model):
    date = models.DateField(default=datetime.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 通过contetentype找到对应的模型
    object_id = models.PositiveIntegerField()  # 记录对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')

