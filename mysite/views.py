from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.shortcuts import render
from read_statistics.utils import *


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取七天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_week_hot_blog()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3660)
        print('cla')
    else:
        print('use cache')

    context['read_nums'] = read_nums
    context['dates'] = dates

    context['hot_data'] = get_today_hot_blog()[:7]
    context['yesterday_hot_data'] = get_yesterday_hot_blog()[:7]
    context['week_hot_data'] = hot_blogs_for_7_days[:7]
    return render(request,'home.html', context)


