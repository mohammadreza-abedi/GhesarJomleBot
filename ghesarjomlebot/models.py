from django.db import models
from django.db.models import CASCADE

from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState


class TelegramUser(AbstractTelegramUser):
    pass


class TelegramChat(AbstractTelegramChat):
    pass


class TelegramState(AbstractTelegramState):
    telegram_user = models.ForeignKey(TelegramUser, related_name='telegram_states', on_delete=CASCADE, blank=True, null=True)
    telegram_chat = models.ForeignKey(TelegramChat, related_name='telegram_states', on_delete=CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('telegram_user', 'telegram_chat')

class UserPost(models.Model):
    file_type = models.CharField("File type", max_length=512,null=True)
    description = models.TextField("Description")
    file_id = models.CharField("File Id", max_length=512)
    OP = models.ForeignKey(TelegramUser,related_name="userPosts",on_delete=models.CASCADE,null=True)
