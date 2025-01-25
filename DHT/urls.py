from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("api", api.Dlist, name='json'),
    path("api/post", api.Dlist, name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/', views.table, name='table'),
    path('myChartTemp/', views.graphiqueTemp, name='myChartTemp'),
    path('myChartHum/', views.graphiqueHum, name='myChartHum'),
    path('chart-data/', views.chart_data, name='chart-data'),
    path('chart-data-jour/', views.chart_data_jour, name='chart-data-jour'),
    path('chart-data-semaine/', views.chart_data_semaine, name='chart-data-semaine'),
    path('chart-data-mois/', views.chart_data_mois, name='chart-data-mois'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin/add-user/', views.add_user, name='add_user'),
    path('admin/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('actions/', views.actions_list, name='actions_list'),
    path('record-action/', views.record_action, name='record_action'),
    path('', views.index, name='index'),  # Page d'accueil
    path('saw', views.home, name='saw'),  # Page principale après connexion
    path('api/get-sensor-data/', views.get_sensor_data, name='get_sensor_data'),
    path('record-action/', views.record_action, name='record_action'),  # Enregistrement des actions
    path('actions-list/', views.actions_list, name='actions_list'),
    path('record-action/', views.record_action, name='record_action'),
    path('actions-list/', views.actions_list, name='actions_list'),
path('api/current-temperature/', views.get_current_temperature, name='current_temperature'),
path('api/today-data/', views.get_today_data, name='today_data'),
path('api/week-data/', views.get_week_data, name='week_data'),
path('api/month-data/', views.get_month_data, name='month_data'),
path('api/data-by-date/', views.chart_data_by_date, name='chart_data_by_date'),
    # Liste des actions pour l'administrateur
]