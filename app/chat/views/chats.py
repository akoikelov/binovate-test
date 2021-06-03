from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from app.chat.models import GroupChat
from app.chat.serializers import CreateChatSerializer, AddParticipantSerializer, RemoveParticipantSerializer


class GroupChatViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CreateChatSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return GroupChat.objects.by_owner(self.request.user)

    @action(detail=True, methods=["POST"], url_path="participants", serializer_class=AddParticipantSerializer)
    def add_participant(self, *args, **kwargs):
        group_chat = self.get_object()

        serializer = AddParticipantSerializer(data=self.request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        serializer.perform(group_chat=group_chat)

        return JsonResponse({
            'success': True
        })

    @action(detail=True, methods=["DELETE"], url_path="participants/(?P<user_id>\\d+)")
    def remove_participant(self, *args, **kwargs):
        serializer = RemoveParticipantSerializer(data={
            'participant': kwargs.get('user_id'),
            'group_chat': kwargs.get('pk')
        }, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        serializer.perform()

        return JsonResponse({
            'success': True
        })
