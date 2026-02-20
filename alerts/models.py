from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=[('low','Low'),('medium','Medium'),('high','High')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user}"
