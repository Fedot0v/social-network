from django.db import models

from social import settings
from utils import create_custom_path
from posts.mixins import UsernameDisplayMixin


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(
        upload_to=create_custom_path,
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.like_set.count()


class Like(models.Model, UsernameDisplayMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                name="unique_like"
            )
        ]
    
    def __str__(self):
        return f"{self.user} liked {self.post}"
    
    @staticmethod
    def toggle_like(user, post):
        like, created = Like.objects.get_or_create(
            user=user,
            post=post
        )
        if not created:
            like.delete()
            return "unliked"
        return "liked"


class Comment(models.Model, UsernameDisplayMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} commented on {self.post}"
    
    @property
    def is_reply(self):
        return self.parent is not None


class CommentReaction(models.Model):
    REACTION_CHOICES = [
        ("like", "👍"),
        ("love", "❤️"),
        ("haha", "😂"),
        ("wow", "😮"),
        ("sad", "😢"),
        ("angry", "😡"),
    ]

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} reacted {self.reaction} to {self.comment}"
