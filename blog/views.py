
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from .forms import RegisterForm, PostForm
from django.urls import reverse
from django.utils import timezone
from .models import Post, about
from django.contrib.auth.models import User
from django.http import Http404 
import markdown 
import re

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    about_ = about.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'about': about_})


def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            # 注册成功，跳转回首页
            return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'blog/register.html', context={'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    md = markdown.markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.text = md.convert(post.text)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/post_detail.html', {'post': post})


def profile(request):
    user = get_object_or_404(User, id=request.session['user_id'])
    posts = Post.objects.filter(author=user).order_by('published_date')
    return render(request, 'blog/profile.html', {'posts': posts, 'user': user})

def post_new(request):
    if not request.session.get('is_login', None):
        return redirect('login')
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})




def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user == post.author):
        raise Http404
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.session.get('is_login', None):
        return redirect('login')
    elif not (request.user == post.author):
        raise Http404
    post.delete()
    return redirect('profile')





       
