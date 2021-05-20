from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Group, Post, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Создаем отдельный базовый mixin."""
    pass


class PostViewSet(ModelViewSet):
    """Проверяем доступность всех публикаций для всех пользователей."""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """Проверяем доступность всех комментариев для всех пользователей."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        return post.comments.all()


class GroupViewSet(CustomViewSet):
    """Получаем список всех групп."""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)


class FollowViewSet(CustomViewSet):
    """Получаем список всех подписчиков и тех на кого они подписаны."""
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.pk)
        return user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
