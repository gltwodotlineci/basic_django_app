from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    Attributes:
        uuid (UUIDField): A unique identifier for the user.
        email (EmailField): The user's email address.
    """
    uuid = models.UUIDField(primary_key=True,
                            unique=True,
                            default=uuid4,
                            editable=False)
    email = models.EmailField(max_length=100,
                              unique=True,
                              blank=True,
                              null=True,
                              verbose_name='email')


class Ticket(models.Model):
    """
    Model representing a ticket that will be created by a user.
    Attributes:
        uuid (UUIDField): A unique identifier for the ticket.
        user (ForeignKey): The user who created the ticket.
        description (TextField): A description of the ticket.
        title (CharField): The title of the ticket.
        image (ImageField): An image associated with the ticket.
        time_created (DateTimeField): The time when the ticket was created.
        time_updated (DateTimeField): Updating time of the ticket.
    """
    uuid = models.UUIDField(primary_key=True,
                            unique=True,
                            default=uuid4,
                            editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='ticket',
                             verbose_name='utilisateur'
                             )
    description = models.TextField(max_length=350)
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


class Review(models.Model):
    """
    Model representing a review for a ticket. It will be created by a user.
    and will be linked to a ticket.
    Attributes:
        uuid (UUIDField): A unique identifier for the review.
        user (ForeignKey): The user who wrote the review.
        ticket (ForeignKey): The ticket being reviewed.
        rating (PositiveSmallIntegerField): The rating given to the ticket.
        headline (CharField): The headline of the review.
        body (TextField): The body of the review.
        time_created (DateTimeField): The time when the review was created.
    """
    uuid = models.UUIDField(primary_key=True,
                            unique=True,
                            default=uuid4,
                            editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='review',
                             verbose_name='utilisateur'
                             )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,
                               unique=True,
                               related_name='review',
                               verbose_name='billet')
    rating = models.PositiveSmallIntegerField(max_length=1024,
                                              validators=[
                                                  MinValueValidator(0),
                                                  MaxValueValidator(5)
                                                  ])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """
    This model is used to manage the follow relationships between users.
    There will be a unique constraint on the combination of user and
    followed_user.
    Attributes:
        uuid (UUIDField): A unique identifier for the follow relationship.
        user (ForeignKey): The user who is following another user.
        followed_user (ForeignKey): The user being followed.
    """
    uuid = models.UUIDField(primary_key=True,
                            unique=True,
                            default=uuid4,
                            editable=False)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'followed_user'],
                                    name='unique_user_follow')]
