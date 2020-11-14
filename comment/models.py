import threading
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class SendMail(threading.Thread):
    """封装多线程"""

    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        # 执行本身初始化函数
        threading.Thread.__init__(self)

    def run(self):  # 当执行多线程时，会自动执行run函数
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )


class Comment(models.Model):
    # 关联到别的模型，可以评论所有东西
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 通过contetentype找到对应的模型
    object_id = models.PositiveIntegerField()  # 记录对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')
    # 评论内容
    text = models.TextField()
    content_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments",
                             on_delete=models.CASCADE)
    root = models.ForeignKey('self', related_name='root_comment', null=True, blank=True,
                             on_delete=models.CASCADE)

    parent = models.ForeignKey('self', related_name='parent_comment', blank=True, null=True,
                               on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", blank=True, null=True,
                                 on_delete=models.CASCADE)

    def send_email(self):
        # 发送邮件通知·
        if self.parent is None:
            # 评论博客的
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论的
            subject = '有人回复你的评论'
            email = self.reply_to.email

        # 5个参数为：主题、邮件内容、发送的邮箱（settings中已经设置好了）、要发送到哪个邮箱、发送错误是否抛出错误
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()  # 反向解析得到链接
            text = render_to_string('comment/send_mail.html', context)

            send_mail = SendMail(subject, text, email)
            send_mail.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-content_time']
