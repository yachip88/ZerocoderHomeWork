from django.shortcuts import render

from .models import Post


def post_list(request):
    posts = Post.objects.select_related("author")
    return render(request, "post_list.html", {"posts": posts})
