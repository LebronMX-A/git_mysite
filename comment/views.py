from django.http import JsonResponse
from comment.models import Comment
from .forms import CommentForm


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():  # 检查文本框输入的数据是否有效
        # 检查数据，保存数据，实例化一个comment对象
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #发送邮件通知
        comment.send_email()

        data['username'] = request.user.get_nickname_or_username()
        data['comment_time'] = comment.content_time.timestamp()#从格林威治时间1970/1/1/00时00分//00秒开始算
        data['text'] = comment.text
        data['status'] = 'Success'

        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'Error'
        data['message'] = list(comment_form.errors.values())[0][0]
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
    return JsonResponse(data)


"""    referer = request.META.get('HTTP_REFERER', reverse('home'))

    content_type = request.POST.get('content_type', '')
    # model_class = ContentType.objects.get(model=content_type).model_class()#不仅仅可以对blog模型评论具体的模型
    # model_obj = model_class.objects.get(pk=object_id)

    # 检查数据
    if not request.user.is_authenticated:
        return render(request,'error.html',{'message': '用户未登录','redirect_to': referer})
    text = request.POST.get('text', '').strip()#去除空格后判断文本框内有无内容

    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空','redirect_to': referer})
    try:
        object_id = int(request.POST.get('object_id', ''))  # 或得到的是字符串，要转成int
        content_object = Blog.objects.get(pk=object_id)
    except Exception :
        return render(request, 'error.html', {'message': '评论对象不存在','redirect_to': referer})

    # 检查数据，保存数据，实例化一个comment对象
    comment = Comment()
    comment.user = request.user
    comment.text = text
    # comment.content_object = model_obj
    comment.content_object = content_object
    comment.save()
    return redirect(referer)"""
