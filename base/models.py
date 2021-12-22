from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[0:50]

    class Meta:
        ordering = ['completed', '-creation']