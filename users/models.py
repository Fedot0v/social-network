from datetime import date

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils import create_custom_path


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self._create_user(email, password, **extra_fields)
    
    
class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=150)
    is_superuser = models.BooleanField(_("superuser"), default=False)
    is_staff = models.BooleanField(_("is_staff"), default=False)
    is_online = models.BooleanField(_("is_online"), default=False)
    
    USERNAME_FIELD = "email"
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def set_online(self):
        self.is_online = True
        self.save()
        
    def set_offline(self):
        self.is_online = False
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = models.ImageField(
        _("profile image"),
        upload_to=create_custom_path,
        blank=True,
        null=True
    )
    bio = models.TextField(_("bio"), blank=True)
    birth_date = models.DateField(_("birth_date"), blank=True, null=True)
    status = models.CharField(_("status"), max_length=50, blank=True)
    location = models.CharField(_("location"), max_length=50, blank=True)

    def clean_birth_date(self):
        if self.birth_date and self.birth_date > date.today():
            raise ValueError("Birth date cannot be in the future.")
        if self.birth_date and self.birth_date < date(1900, 1, 1):
            raise ValueError("Birth date cannot be earlier than 1900.")
        return self.birth_date
    
    def clean(self):
        self.clean_birth_date()
        super().clean()
        
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (
                    self.birth_date.month,
                    self.birth_date.day
                )
            )
        return None

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return self.get_full_name
