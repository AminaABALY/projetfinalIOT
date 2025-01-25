from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from django.core.mail import send_mail
from django.conf import settings  # N'oubliez pas d'importer settings
import requests


@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        # Récupérer toutes les données et les sérialiser
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)
        return Response(data_ser.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            # Enregistrer les données sérialisées
            serial.save()

            # Vérifier si des données existent
            derniere_ligne = Dht11.objects.last()
            if derniere_ligne:
                derniere_temperature = derniere_ligne.temp
                print(f"Dernière température : {derniere_temperature}")

                # Vérifier si la température dépasse 25
                if derniere_temperature > 25:
                    subject = 'Alerte'
                    message = (
                        'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement '
                        'pour vérifier et corriger cette situation.'
                    )
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['farajrayhan@gmail.com']

                    try:
                        # Envoyer une alerte WhatsApp via Twilio
                        account_sid = 'AC90ec92a4fd9b592d0682506fccfb8683'
                        auth_token = 'a2028c1c2b88acefbd7596f77804cb8f'
                        client = Client(account_sid, auth_token)

                        message_whatsapp = client.messages.create(
                            from_='whatsapp:+14155238886',
                            body=(
                                'Il y a une alerte importante sur votre Capteur : '
                                'la température dépasse le seuil.'
                            ),
                            to='whatsapp:+212646750352'
                        )
                        print(f"Message envoyé avec SID : {message_whatsapp.sid}")

                    except Exception as e:
                        print(f"Erreur lors de l'envoi du message WhatsApp : {e}")
                        return Response(
                            {"error": "Erreur lors de l'envoi de l'alerte WhatsApp."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

                    # Envoi d'email
                    send_mail(subject, message, email_from, recipient_list)

            return Response(serial.data, status=status.HTTP_201_CREATED)

        else:
            # Si les données ne sont pas valides
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response

telegram_token = '8008679397:AAH1rc-GedxKlbxvh2NcR5gGYEZD41agKeM'
chat_id = '5419149633'
telegram_message = ('La température dépasse le seuil de 10°C ,Veuillez intervenir immédiatement'
                    'pour vérifier et corriger cette situation')
send_telegram_message(telegram_token, chat_id, telegram_message)
