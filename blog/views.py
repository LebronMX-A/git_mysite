from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator  # django 内置的分页器
from blog.models import Blog, BlogType
from read_statistics.models import ReadNum, ReadDetail

def get_blog_list_common_data(request, blog_all_list):
    context = {}
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10个博客分一个页面
    current_page = request.GET.get('page', 1)  # 获取当前页面参数
    pages_of_blog = paginator.get_page(current_page)  # 不用考虑是数字和英文,出错之后自动返回一
    current_page_num = pages_of_blog.number  # 通过paginator的属性number来获取当前的页面
    # 让前端页面的页码展示不要过多，只要当前页面的前两个和后两个就可，1和最后一页特殊
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num,
                            min(current_page_num + 2, paginator.num_pages) + 1))  # paginator的属性num_pages可以知道页面的分页数

    if page_range[0] - 1 >= 2:  # 如果第一个数和第二个数相差大于二，所以就要有省略号了
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:  # 如果第一个数和第二个数相差大于二，所以就要有省略号了
        page_range.append('...')
    if page_range[0] != 1:  # 如果第一个不是一就插入一
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:  # 如果最后一个不是最后一页，就把最后一页的页码加上去
        page_range.append(paginator.num_pages)
    # 加上省略的标记页码

    # 获取博客分类的数量
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()  # 暂时给Blog_type怎加一个字段，计算分类的数量
        blog_types_list.append(blog_type)
    # 获取日期归档的对应的博客数量
    blog_date_dict = {}  # 通过一个字典的键值对，一个时期对应一个月博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_count

    context['page_range'] = page_range
    context['pages_of_blog'] = pages_of_blog  # 前端通过这个获取每一页的文章，还可以通过分页器得到一共有多少的文章
    context['blogs'] = pages_of_blog.object_list  # 每一页的文章
    context['blog_dates'] = blog_date_dict  #
    context['blog_types'] = blog_types_list

    return context


def blog_list(request):
    blog_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blog_list)
    return render(request, "blog/blog_list.html", context)


def blogs_with_type(request, blog_type_pk):
    blogs_type = get_object_or_404(BlogType, pk=blog_type_pk)  # 有可能获取不到，所以用get_object_or_404
    blog_all_list = Blog.objects.filter(blog_type=blogs_type)  # filter筛选,根据类型来帅选blog_type,如何得到blog_type？？？
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blogs_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)  # filter筛选,年和月份来筛选博客
    context = get_blog_list_common_data(request, blog_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):  # 要查询的model,后面的blog_pk＝1是查询条件，你可以根据你需要查询的情况来写条件
    blog = get_object_or_404(Blog, pk=blog_pk)  # 按照pk来查询

    # 实现阅读数的计算
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        ct = ContentType.objects.get_for_model(Blog)
        # 总阅读数加一
        readnum, create = ReadNum.objects.get_or_create(content_type=ct,
                                                        object_id=blog_pk)  # 等价于下面的办法，更加简便，返回一个元祖，一个列表和是否存在
        # if(ReadNum.objects.filter(content_type=ct,object_id=blog_pk).count()):
        #     # 存在记录
        #     readnum = ReadNum.objects.get(content_type=ct,object_id=blog_pk)
        # else:
        #     #不存在记录
        #     readnum=ReadNum(content_type=ct,object_id=blog_pk)
        # 计数加一
        readnum.read_num += 1
        readnum.save()
        date = timezone.now().date()
        # 当天阅读数加一
        readdetail, creates = ReadDetail.objects.get_or_create(date=date, content_type=ct, object_id=blog_pk)
        # if ReadDetail.objects.filter(date=date,content_type=ct,object_id=blog_pk).count():
        #     readdetail=ReadDetail.objects.get(date=date,content_type=ct,object_id=blog_pk)
        # else:
        # readdetail = ReadDetail(content_type=ct, object_id=blog_pk,date=date)
        readdetail.read_num += 1
        readdetail.save()

    context = {}
    # 实现上一页下一页
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()  # 筛选比当前博客的时间晚的博客 __gt表示大于 greater than
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()  # 筛选比当前博客的时间晚的博客 __lt表示大于 greater than
    context['blog'] = blog  # 增加所有博客的信息


    respone = render(request, "blog/blog_detail.html", context)
    respone.set_cookie('blog_%s_readed' % blog_pk, 'true')  # 类似字典来保存cookie key value

    return respone
