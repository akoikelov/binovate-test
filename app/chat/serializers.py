from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from app.chat.models import Message, GroupChat


class CreateMessageSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=User.objects.all(), required=False)
    group_chat = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=GroupChat.objects.all(), required=False)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Message
        fields = ('text', 'user', 'group_chat', 'author')

    def validate(self, attrs):
        self.validate_user_group_chat(attrs)

        return attrs

    def validate_user_group_chat(self, attrs):
        if attrs.get('user') is None and attrs.get('group_chat') is None:
            raise serializers.ValidationError('At least user or group_chat should be set')

        if attrs.get('user') and attrs.get('group_chat'):
            raise serializers.ValidationError('Either user OR group_chat entity can be set')

    def validate_group_chat(self, value):
        user = self.context['request'].user

        if not value.participants.filter(id=user.id).exists() and value.owner != user:
            raise ValidationError('Only owner and participants of the chat can send message to the given chat')

        return value


class ListMessageSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'text', 'user', 'group_chat', 'author')

    def get_author(self, obj):
        return obj.author.username


class CreateChatSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = GroupChat
        fields = ('name', "owner")

        validators = [
            UniqueTogetherValidator(
                queryset=GroupChat.objects.all(),
                fields=["name", "owner"],
                message="Group chat with given name already exists",
            )
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)

        instance.participants.add(self.context['request'].user)

        return instance


class AddParticipantSerializer(serializers.Serializer):

    participant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def perform(self, group_chat: GroupChat):
        group_chat.participants.add(self.validated_data['participant'])


class RemoveParticipantSerializer(serializers.Serializer):

    participant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group_chat = serializers.PrimaryKeyRelatedField(queryset=GroupChat.objects.all())

    def validate(self, attrs):
        if attrs['group_chat'].owner == attrs['participant']:
            raise ValidationError('Owner of the chat cannot be removed from participants list')

        return attrs

    def perform(self):
        self.validated_data['group_chat'].participants.remove(self.validated_data['participant'])
