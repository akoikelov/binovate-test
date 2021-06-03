from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework_swagger.views import get_swagger_view

from app.chat.views.chats import GroupChatViewSet
from app.chat.views.messages import MessageViewSet

schema_view = get_swagger_view(title='Pastebin API')

router = SimpleRouter(trailing_slash=False)
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'group-chat', GroupChatViewSet, basename='group_chat')

urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('v1/', include([
        path('auth/api-token-auth', obtain_jwt_token),
        path('auth/', include('rest_framework.urls', namespace='rest')),
        path('', include(router.urls))
    ])),
]