from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True, verbose_name='email')


class Ticket(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4,  editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='ticket',
                             verbose_name='utilisateur'
                             )
    description = models.TextField(max_length=350)
    title = models.CharField(max_length=128)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4,  editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='review',
                             verbose_name='utilisateur'
                             )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='review', verbose_name='billet')#unique=True
    rating = models.PositiveSmallIntegerField(max_length=1024, validators=[
        MinValueValidator(0), MaxValueValidator(5)
    ])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4,  editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following',
                             verbose_name='utilisateur'
                             )
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='followed_user',
                             verbose_name='utilisateur'
                             )
    
    class Meta: # 'Unique together' à l'utiliser
        constraints = [
            models.UniqueConstraint(fields=['user', 'followed_user'], name='unique_user_follow')
        ]
