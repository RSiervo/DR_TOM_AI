from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Consultation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="consultations", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    symptoms_text = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    result_text = models.TextField(blank=True)

    def __str__(self):
        who = self.user.username if self.user else "anon"
        return f"Consultation #{self.id} by {who} - {self.created_at:%Y-%m-%d %H:%M}"

    def get_absolute_url(self):
        return reverse("consultation_detail", args=[self.id])
