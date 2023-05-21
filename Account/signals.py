from django.contrib import messages
from django.contrib.auth import user_logged_out, user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import Account, Profile


@receiver(post_save, sender=Account)
def create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)