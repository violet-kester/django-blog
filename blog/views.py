from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    "Retrieves all published Posts."

    posts = Post.objects.filter(status='PB')
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    "Retrieves individual published Post by ID."

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
