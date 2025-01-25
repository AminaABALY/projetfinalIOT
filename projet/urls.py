from django.contrib import admin

from django.urls import path,include

from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DHT.urls')),

    path('api/', include('sensor.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include('sensor.urls'))




]

