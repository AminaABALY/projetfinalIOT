from django.db import models
from django.contrib.auth.models import User

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date}: {self.temperature}°C, {self.humidity}%"
class Incident(models.Model):
    operator = models.CharField(max_length=100)
    remark = models.TextField(blank=True)
    acquisition_date = models.DateTimeField(auto_now_add=True)
    incident_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Incident créé par {self.created_by} - {self.incident_date}"