from django.urls import path
from . import views

from .views import SensorDataView, LastSensorDataView

urlpatterns = [
    path('data/', SensorDataView.as_view(), name='sensor_data'),  # Route pour GET/POST toutes les données
    path('data/last/', LastSensorDataView.as_view(), name='last_sensor_data'),  # Route pour GET la dernière donnée
]
