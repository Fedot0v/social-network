from rest_framework import serializers
from users.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "full_name", "is_online"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image", "bio", "location", "birth_date", "status", "age"]


class ProfileDetailSerializer(ProfileSerializer):
    user = UserSerializer()

    class Meta:
        fields = ProfileSerializer.Meta.fields + ["user"]


class ProfileListSerializer(ProfileSerializer):
    user = UserSerializer()
    is_online = serializers.SerializerMethodField()
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ["is_online"]
        
        def get_is_online(self, obj):
            return obj.user.is_online
