# Create your views here.
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from app.chat.models import Message
from app.chat.serializers import CreateMessageSerializer, ListMessageSerializer


class MessageViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = ListMessageSerializer

    def get_serializer_class(self):
        cls = super().get_serializer_class()

        if self.action in ("create",):
            cls = CreateMessageSerializer
        elif self.action == "list":
            cls = ListMessageSerializer

        return cls

    def get_queryset(self):
        user = self.request.user

        return Message.objects.related_to_user(user)

