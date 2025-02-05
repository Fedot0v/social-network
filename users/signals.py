from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from users.models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(user_logged_in, sender=User)
def user_logged_in_handler(sender, request, user, **kwargs):
    user.set_online()

@receiver(user_logged_out, sender=User)
def user_logged_out_handler(sender, request, user, **kwargs):
    user.set_offline()
