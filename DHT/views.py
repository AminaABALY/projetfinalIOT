from django.shortcuts import render
from django.db.models import Min, Max
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import ActivityLog
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import ActivityLog
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.utils.timezone import now
import json
from .models import IncidentAction
from django.contrib.auth import authenticate, login, logout






from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



def get_sensor_data(request):
    # Récupérer les 100 dernières entrées, triées par date décroissante
    data = Dht11.objects.order_by('-dt')[:100]

    if not data.exists():  # Si aucune donnée n'est trouvée
        return JsonResponse({
            "labels": [],
            "temperature": [],
            "humidity": []
        })

    response_data = {
        "labels": [entry.dt.strftime("%Y-%m-%d %H:%M:%S") for entry in data],
        "temperature": [entry.temp for entry in data],
        "humidity": [entry.hum for entry in data],
    }
    return JsonResponse(response_data)
def get_sensor_data_filtered(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    data = SensorData.objects.all()

    if start_date:
        data = data.filter(timestamp__gte=start_date)
    if end_date:
        data = data.filter(timestamp__lte=end_date)

    data = data.order_by('-timestamp')[:100]
    response_data = {
        "labels": [entry.timestamp.strftime("%Y-%m-%d %H:%M:%S") for entry in data],
        "temperature": [entry.temperature for entry in data],
        "humidity": [entry.humidity for entry in data],
    }
    return JsonResponse(response_data)



def home(request):
    # Récupérer toutes les valeurs du modèle Dht11
    data = Dht11.objects.all()

    # Récupérer la dernière ligne (dernière entrée dans la base de données)
    derniere_ligne = Dht11.objects.last()

    if derniere_ligne:
        # Récupérer la température et l'humidité de la dernière ligne
        temp = derniere_ligne.temp
        hum = derniere_ligne.hum
        derniere_date = derniere_ligne.dt

        # Calculer le temps écoulé
        delta_temps = timezone.now() - derniere_date
        difference_minutes = delta_temps.seconds // 60
        temps_ecoule = f'il y a {difference_minutes} min'
        if delta_temps.days > 0:
            temps_ecoule = f'il y a {delta_temps.days} j {difference_minutes // 60} h {difference_minutes % 60} min'

        # Récupérer les valeurs min et max pour la température et l'humidité
        min_temp = Dht11.objects.aggregate(Min('temp'))['temp__min']
        max_temp = Dht11.objects.aggregate(Max('temp'))['temp__max']
        min_hum = Dht11.objects.aggregate(Min('hum'))['hum__min']
        max_hum = Dht11.objects.aggregate(Max('hum'))['hum__max']
    else:
        # Si aucune donnée n'est présente dans la base, afficher un message
        temp = hum = min_temp = max_temp = min_hum = max_hum = "Données non disponibles"
        temps_ecoule = "Données non disponibles"

    # Passer les données au template
    return render(request, 'home.html', {
        'data': data,
        'temp': temp,
        'hum': hum,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'min_hum': min_hum,
        'max_hum': max_hum,
        'temps_ecoule': temps_ecoule,
    })
def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})

def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
#pour afficher navbar de template
def index(request):
    return render(request, 'index.html')

#pour afficher les graphes
def graphiqueTemp(request):
    return render(request, 'ChartTemp.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def graphiqueHum(request):
    return render(request, 'ChartHum.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def chart_data(request):
    dht = Dht11.objects.all().order_by('dt')  # Trier par date croissante
    data = {
        'temps': [entry.dt.strftime('%Y-%m-%d %H:%M:%S') for entry in dht],
        'temperature': [entry.temp for entry in dht],
        'humidity': [entry.hum for entry in dht],
    }
    return JsonResponse(data)


#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()

    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)

    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_data_mois(request):
    dht = Dht11.objects.all()

    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def sendtele():
    token = '6662023260:AAG4z48OO9gL8A6szdxg0SOma5hv9gIII1E'
    rece_id = 1242839034
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('home')  # Remplacez 'home' par le nom de votre page d'accueil
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def record_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            operator = data.get('operator', 'Unknown')
            remark = data.get('remark', '')
            action = data.get('action', 'Unknown')

            # Enregistrez l'action dans la base de données
            IncidentAction.objects.create(
                operator=operator,
                remark=remark,
                action=action,
                timestamp=now()
            )

            return JsonResponse({"message": "Action enregistrée avec succès!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # Permettre temporairement les requêtes GET pour tester
    if request.method == "GET":
        return JsonResponse({"message": "API en ligne, utilisez POST pour envoyer des données."})

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
def actions_list(request):
    # Récupérer toutes les actions enregistrées dans la base de données
    actions = IncidentAction.objects.all().order_by('-timestamp')  # Tri décroissant par date
    return render(request, 'actions_list.html', {'actions': actions})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin-dashboard')  # Tableau de bord administrateur
            else:
                return redirect('home')  # Tableau de bord utilisateur
        else:
            return render(request, 'login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')  # Redirige si l'utilisateur n'est pas un administrateur
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

@login_required
def add_user(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Vous n'avez pas la permission d'effectuer cette action.")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': "Nom d'utilisateur déjà pris."}, status=400)
        User.objects.create_user(username=username, password=password)
        return redirect('admin_dashboard')
    return render(request, 'add_user.html')

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Vous n'avez pas la permission d'effectuer cette action.")
    try:
        user = User.objects.get(id=user_id)
        if user.is_staff:  # Ne pas supprimer un administrateur
            return JsonResponse({'error': "Impossible de supprimer un administrateur."}, status=400)
        user.delete()
        return redirect('admin_dashboard')
    except User.DoesNotExist:
        return JsonResponse({'error': "Utilisateur non trouvé."}, status=404)
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirige vers la page de connexion après inscription
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def user_dashboard(request):
    if request.user.is_staff:
        # Redirige les administrateurs vers le tableau de bord administrateur
        return redirect('/admin-dashboard/')
    return render(request, 'user_dashboard.html')
def actions_list(request):
    actions = IncidentAction.objects.all().order_by('-timestamp')  # Récupère toutes les actions
    return render(request, 'actions_list.html', {'actions': actions})
def get_current_temperature(request):
    latest_data = Dht11.objects.last()
    if latest_data:
        return JsonResponse({'temperature': latest_data.temp})
    return JsonResponse({'temperature': None})
def get_today_data(request):
    today = now().date()
    data = Dht11.objects.filter(dt__date=today).order_by('dt')
    response_data = {
        'labels': [entry.dt.strftime("%Y-%m-%d %H:%M:%S") for entry in data],
        'temperature': [entry.temp for entry in data],
        'humidity': [entry.hum for entry in data],
    }
    return JsonResponse(response_data)

def get_week_data(request):
    start_of_week = now() - timedelta(days=7)
    data = Dht11.objects.filter(dt__gte=start_of_week).order_by('dt')
    response_data = {
        'labels': [entry.dt.strftime("%Y-%m-%d %H:%M:%S") for entry in data],
        'temperature': [entry.temp for entry in data],
        'humidity': [entry.hum for entry in data],
    }
    return JsonResponse(response_data)

def get_month_data(request):
    start_of_month = now() - timedelta(days=30)
    data = Dht11.objects.filter(dt__gte=start_of_month).order_by('dt')
    response_data = {
        'labels': [entry.dt.strftime("%Y-%m-%d %H:%M:%S") for entry in data],
        'temperature': [entry.temp for entry in data],
        'humidity': [entry.hum for entry in data],
    }
    return JsonResponse(response_data)
def chart_data_by_date(request):
    selected_date = request.GET.get('date')  # Récupère la date envoyée en paramètre GET
    if selected_date:
        try:
            # Convertir la date reçue en objet datetime
            date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
            # Filtrer les données pour la date sélectionnée
            start_date = make_aware(date_obj)
            end_date = make_aware(date_obj + datetime.timedelta(days=1))
            dht_data = Dht11.objects.filter(dt__range=(start_date, end_date))

            # Préparer les données pour le retour JSON
            data = {
                'labels': [entry.dt.strftime("%Y-%m-%d %H:%M:%S") for entry in dht_data],
                'temperature': [entry.temp for entry in dht_data],
                'humidity': [entry.hum for entry in dht_data],
            }
            return JsonResponse(data)
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)
    else:
        return JsonResponse({"error": "No date provided"}, status=400)