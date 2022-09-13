from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True
    )
    
    title = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

    parent_task = models.ForeignKey(
        "self", 
        blank=True, 
        null=True, 
        default=None, 
        related_name='children_tasks',
        on_delete=models.CASCADE
    )
 
    def __str__(self):
        return f"<Task title='{self.title}' " \
                f"created_at='{self.created_at}'> "
