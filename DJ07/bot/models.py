from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField("ID пользователя Telegram", unique=True)
    name = models.CharField("Имя", max_length=150)

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"
