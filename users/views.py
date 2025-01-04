from django.db.models import Value
from django.db.models.functions import Concat
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from users.models import Profile, User
from users.serializers import (
    ProfileDetailSerializer,
    ProfileListSerializer,
    ProfileSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ["create", "login"]:
            return (AllowAny(),)
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED
        )
    
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
            "message": "Login successful",
            "user": f"{user.first_name} {user.last_name}",
            "token": token.key
            },
            status=status.HTTP_200_OK
        )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        elif self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        query_params = self.request.query_params
        
        filter_kwargs = {
            "first_name": query_params.get("first_name", None),
            "last_name": query_params.get("last_name", None),
            "is_online": query_params.get("is_online", None),
        }
        
        filter_kwargs = {k: v for k, v in filter_kwargs.items() if v is not None}
        
        if "full_name" in query_params:
            full_name = query_params.get("full_name").split()
            queryset = queryset.annotate(
                full_name=Concat(
                    "user__first_name", Value(" "), "user__last_name"
                    ).filter(full_name__iexact=full_name)
            )
        if filter_kwargs:
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset
