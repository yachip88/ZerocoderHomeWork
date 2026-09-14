from django.shortcuts import render

from .models import News_post


def home(request):
    news = News_post.objects.order_by("-pub_date")
    return render(request, "news_home.html", {"news": news})
