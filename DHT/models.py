
# Create your models here.
from django.db import models

from django.contrib.auth.models import User
from django.utils.timezone import now
class Dht11(models.Model):
  temp = models.FloatField(null=True)
  hum = models.FloatField(null=True)
  dt = models.DateTimeField(auto_now_add=True,null=True)



class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=255)  # Exemple: "Acquisition réalisée"
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
class IncidentAction(models.Model):
    operator = models.CharField(max_length=100)  # Nom de l'opérateur
    action = models.CharField(max_length=255)  # Action effectuée
    remark = models.TextField(blank=True, null=True)  # Remarque optionnelle
    timestamp = models.DateTimeField(default=now)  # Date et heure de l'action

    def __str__(self):
        return f"{self.operator} - {self.action}"
