import string
import random
import time
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgetPasswordForm
from django.core.mail import send_mail
from .models import Profile


# 登录的处理方法
def login(request):
    if request.method == 'POST':  # login.html页面发送的登录请求，含有用户名和秘密为post请求
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 验证数据是否有效
            username = login_form.cleaned_data['username_or_email']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)  # 登录验证
            if user is not None:
                auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))  # 获取get参数中他的前一个url，如果没有的话就跳转到主页

    else:  # 如果是从blog_detail页面中发起的登录请求，为get请求
        login_form = LoginForm

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


# 注册的处理方法
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():  # 判断是否有效
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)  # 创建一个用户
            user.save()
            # 清楚session
            del request.session['bind_email_code']
            # 注册完成后自动登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():  # 验证数据是否有效
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = auth.authenticate(request, username=username, password=password)  # 登录验证
        if user is not None:  # 登录成功
            auth.login(request, user)
            data = {}
            data['status'] = "Success"
            return JsonResponse(data)  # 获取get参数中他的前一个url，如果没有的话就跳转到主页
        else:  # 登录不成功
            data = {}
            data['status'] = 'Error'
            data['message'] = "账号密码错误"
            return JsonResponse(data)
    else:  # 验证不通过
        data = {}
        data['status'] = 'Error'
        data['message'] = "登录失败"
        return JsonResponse(data)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))  # 获取get参数中他的前一个url，如果没有的话就跳转到主页


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    redirct_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():  # 这里判断了是否登录和数据是否为空
            nickname_new = form.cleaned_data['nickname_new']
            profile, create = Profile.objects.get_or_create(user=request.user)  # 必须接受两个返回值
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirct_to)
    else:
        form = ChangeNicknameForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirct_to
    return render(request, 'form.html', context)


def bind_email(request):
    redirct_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()

            # 清楚session
            del request.session['bind_email_code']
            return redirect(redirct_to)
    else:
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirct_to
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')  # 获取email
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != "":
        # 生产验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))  # 字母加数字组合四位数字  ''.join将list变为字符串
        request.session['bind_email_code'] = code
        now = int(time.time())
        send_code_now = request.session.get('send_code_time', 0)
        if now - send_code_now <= 30:
            data['status'] = 'Error'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮箱
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                '1472601637@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'Success'
    else:
        data['status'] = "Error"
    return JsonResponse(data)


def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)  # 获取form表单
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def forget_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清楚session
            del request.session['forget_password_code']
            return redirect(redirect_to)
    else:
        form = ForgetPasswordForm()
    context = {}
    context['page_title'] = '找回密码'
    context['form_title'] = '找回密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forget_password.html', context)
