from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TodoItem(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='todo_items'
    )

    post = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
