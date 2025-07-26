from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, ConversationEventViewSet

router = DefaultRouter()

router.register(r'api/conversation', ConversationViewSet, basename='conversation')

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

event_list = ConversationEventViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
event_detail = ConversationEventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', include(router.urls)),
    path('api/conversation/<int:conversation_pk>/message/', message_list, name='message-list'),
    path('api/conversation/<int:conversation_pk>/message/<int:pk>/', message_detail, name='message-detail'),
    path('api/conversation/<int:conversation_pk>/conversation-event/', event_list, name='event-list'),
    path('api/conversation/<int:conversation_pk>/conversation-event/<int:pk>/', event_detail, name='event-detail'),
]
