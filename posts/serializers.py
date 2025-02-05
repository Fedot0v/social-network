from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ReadOnlyField,
    ListSerializer,
    IntegerField,
    Serializer,
    URLField
)

from posts.models import (
    Post,
    Like,
    Comment,
    CommentReaction
)
from users.serializers import UserSerializer


class ImageSerializer(Serializer):
    url = URLField()


class PostListSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    likes_count = IntegerField(source='likes_count', read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "likes_count",
            "created_by",
        ]


class PostRetrieveSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    likes_count = IntegerField(source='likes_count', read_only=True)
    image = ImageSerializer(source='image', read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "likes_count",
            "created_by",
            "image",
        ]

class LikeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    username_display = SerializerMethodField()
    
    class Meta:
        model = Like
        fields = [
            "id",
            "post",
            "created_at",
            "get_username_display",
        ]
    
    def get_username_display(self, obj):
        return obj.get_username_display


class CommentListSerializer(ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class BaseCommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    username_display = ReadOnlyField(source="get_username_display")
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "content",
            "parent",
            "created_at",
            "is_reply",
            "replies",
            "username_display",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "is_reply",
            "replies",
            "username_display",
        ]
    
    def get_replies(self, obj):
        """Получение всех ответов на комментарий, если он не является ответом."""
        if obj.is_reply:
            return None
        return CommentSerializer(
            obj.comment_set.all(),
            many=True
        ).data


class CommentSerializer(BaseCommentSerializer):
    list_serializer_class = CommentListSerializer


class CommentRetrieveSerializer(BaseCommentSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'username_display', 'replies']
        read_only_fields = ['user', 'created_at', 'replies']


class CommentReactionSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    username_display = ReadOnlyField(source="get_username_display")

    class Meta:
        model = CommentReaction
        fields = [
            "id",
            "comment",
            "user",
            "reaction",
            "created_at"
        ]
        read_only_fields = ["user", "created_at"]
