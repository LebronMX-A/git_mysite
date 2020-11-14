from django.db.models import Sum
from blog.models import Blog
from django.utils import timezone
from .models import ReadDetail
import datetime


# 这几个函数都是统计不同时间的阅读量，都展示在home，这几个函数都在mysite的views的home函数中使用


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, -1, -1):
        date = today - datetime.timedelta(days=i)  # 天数的差值，参数为几天
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_blog():
    today = timezone.now().date()
    # 统计七天内被阅读数量比较高的博客
    today_hot_blogs = Blog.objects.filter(read_details__date=today).values('id', 'title').annotate(
        read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return today_hot_blogs


def get_yesterday_hot_blog():
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    # 统计七天内被阅读数量比较高的博客
    yesterday_hot_blogs = Blog.objects.filter(read_details__date=yesterday, read_details__date__gte=yesterday).values('id','title').annotate(
        read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return yesterday_hot_blogs


def get_week_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # 统计七天内被阅读数量比较高的博客
    week_hot_blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gte=date).values('id',
                                                                                                             'title').annotate(
        read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return week_hot_blogs




"""get_week_hot_blog是对get_7_hot_data的查询优化，get_7_hot_data方法不能展示出热门博客的标题，
在blog models加入GenericForeignKey可以反向通过Read_Details该模型关联到Blog模型上面
反向通用关系类GenericRelation

def get_7_hot_data(content_type):
    today = timezone.now().date()
    date=today-datetime.timedelta(days=7)
    read_details=ReadDetail.objects.filter(content_type=content_type,date__lte=today,date__gte=date).values('content_type','object_id').annotate(read_num_sum=Sum('read_num')).order_by('-read_num')
    return read_details

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details

def get_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details"""