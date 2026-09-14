from django.http import HttpResponse
from django.shortcuts import render


def data(request):
    return render(request, "data.html")


def test(request):
    return HttpResponse("Это страница test: здесь проверка маршрутов Django.")
