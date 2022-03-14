from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from .mixins import ListCreateViewSet
from .permissions import AuthorOrReadOnlyPermission

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnlyPermission, ]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnlyPermission, ]
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])


class FollowViewSet(ListCreateViewSet):
    serializer_class = serializers.FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['following__username', ]

    def perform_create(self, serializer):
        if 'following' not in self.request.data:
            raise ParseError(
                detail='Ошибка в запросе, укажите параметр following'
            )
        try:
            author = User.objects.get(username=self.request.data['following'])
        except User.DoesNotExist:
            raise ParseError(detail='Нет автора с таким именем')

        if self.request.user == author:
            raise ParseError(
                detail='Нельзя подписаться на самого себя'
            )
        if Follow.objects.filter(
                user=self.request.user, following=author).exists():
            raise ParseError(
                detail='Нельзя подписаться на автора дважды'
            )
        serializer.save(user=self.request.user,
                        following=author)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
