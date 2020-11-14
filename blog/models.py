from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from read_statistics.models import ReadNum, ReadNumExpend, ReadDetail
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)  # 一篇文章对应一种类型

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpend):  # 继承ReadNumExpend类，可以获得get_read_num的方法
    # 标题
    title = models.CharField(max_length=50)
    # 博客类型，外键，关联到博客类型
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    # 内容
    read_details = GenericRelation(ReadDetail)
    # read_details = GenericRelation(ReadDetail)反向关联到ReadDetail
    content = RichTextUploadingField()  # 将charfield替换为RichTextField  RichTextField不允许上传文件
    # 作者，用django自带的模型，链接外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 最后修改时间
    last_updata_time = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-create_time']  # 按照创建时间排序


"""class ReadNum(models.Model):
    # 统计阅读数量
    read_num = models.IntegerField(default=0)
    blog=models.OneToOneField(Blog,on_delete=models.CASCADE)"""
