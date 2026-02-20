from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        default="default.png",
        blank=True,
        null=True
    )

    age = models.IntegerField(null=True, blank=True)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

    # ---- Optional helper (recommended)
    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return "/media/default.png"
