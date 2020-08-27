
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from .forms import RegisterForm, PostForm
from django.urls import reverse
from django.utils import timezone
from .models import Post, about
from django.contrib.auth.models import User
from django.http import Http404 
import markdown 
import re

def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    about_ = about.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'about': about_})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', context={'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.text = markdown.markdown(post.text, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
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





       
