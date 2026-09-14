from django.http import HttpResponse


def users_count(request):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return HttpResponse(f"Пользователей в системе: {User.objects.count()}")
