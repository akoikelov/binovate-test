from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class MessageQuerySet(models.QuerySet):

    def related_to_user(self, user: User):
        return self.filter(Q(author=user) | Q(user=user) |
                           Q(group_chat__participants__in=[user]) |
                           Q(group_chat__owner=user))


class MessageManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def related_to_user(self, user: User):
        return self.get_queryset().related_to_user(user)


class GroupChatQuerySet(models.QuerySet):

    def by_owner(self, user: User):
        return self.filter(owner=user)


class GroupChatManager(models.Manager):
    def get_queryset(self):
        return GroupChatQuerySet(self.model, using=self._db)

    def by_owner(self, user: User):
        return self.get_queryset().by_owner(user)