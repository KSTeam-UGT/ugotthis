# pylint: disable=E1101
from django.db import models
from django.contrib.auth.models import User


class UserSetting(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    keywords = models.CharField(max_length=160)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keywords
