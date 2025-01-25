from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer
from rest_framework import status



class SensorDataView(APIView):
    # Méthode GET pour récupérer toutes les données
    def get(self, request):
        data = SensorData.objects.all()  # Récupère toutes les données
        serializer = SensorDataSerializer(data, many=True)  # Sérialise les données
        return Response(serializer.data)  # Renvoie les données sérialisées sous forme de réponse

    # Méthode POST pour ajouter de nouvelles données
    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)  # Sérialise les données reçues dans la requête
        if serializer.is_valid():  # Vérifie si les données sont valides
            serializer.save()  # Sauvegarde les données dans la base de données
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)  # Répond avec les données et un statut 201 (créé)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)  # Si les données ne sont pas valides, renvoie une erreur 400
class LastSensorDataView(APIView):
    def get(self, request):
        try:
            # Récupère la dernière donnée postée (la plus récente)
            last_data = SensorData.objects.latest('date')  # Trie par date et récupère la dernière entrée
            serializer = SensorDataSerializer(last_data)
            return Response(serializer.data)  # Retourne les données sérialisées
        except SensorData.DoesNotExist:
            # Si aucune donnée n'existe dans la base de données
            return Response({"error": "Aucune donnée trouvée"}, status=404)
from django.http import JsonResponse

def get_last_data(request):
    # Récupère les données à partir de ta base de données ou autre
    data = {'last_data': 'some data'}
    return JsonResponse(data)
