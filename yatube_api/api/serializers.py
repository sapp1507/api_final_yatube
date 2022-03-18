from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True, default=None
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ['user', 'following']
        model = Follow

    def validate(self, attrs):
        request = self.context['request']

        if 'following' not in request.data:
            raise serializers.ValidationError(
                'Ошибка в запросе, укажите параметр following'
            )
        try:
            author = User.objects.get(username=request.data['following'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Нет автора с таким именем')

        if author == request.user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')

        if request.user.follower.filter(following=author).exists():
            raise serializers.ValidationError(
                f'Вы уже подписались на автора {author}'
            )

        return attrs
