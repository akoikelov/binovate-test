from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from app.chat.managers import MessageManager, GroupChatManager


class GroupChat(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    participants = models.ManyToManyField(User, related_name='group_chats', verbose_name='Participants')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_group_chats', verbose_name='Owner')

    objects = GroupChatManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "owner"], name="group_chat_name_owner_unique")
        ]

    def __unicode__(self):
        return self.name


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Author')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                             verbose_name='User', null=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages',
                                   verbose_name='Group Chat', null=True)

    objects = MessageManager()

    def __unicode__(self):
        return self.text
