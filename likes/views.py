from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog
from .models import LikeCount, LikeRecord


# Create your views here.

def SuccessResponse(liked_num):
    data = {}
    data['status'] = "Success"
    data['liked_num'] = liked_num
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'Error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        ct = ContentType.objects.get_for_model(Blog)
        ct = ContentType.objects.filter(model=content_type).first()
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')
    # 处理数据
    if request.GET.get('is_like') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=ct, object_id=object_id,
                                                                user=user)  # 返回创建对象，和是否为创建还是获取
        # 要点赞
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)

        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')
    else:
        # 要取消点赞
        if LikeRecord.objects.filter(content_type=ct, object_id=object_id, user=user).exists():
            # 有过点赞，要取消
            like_record = LikeRecord.objects.get(content_type=ct, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数减一
            like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')

        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'you were not liked')
