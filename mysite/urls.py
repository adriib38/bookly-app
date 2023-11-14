from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Incluye las rutas de la aplicación myapp
    path('', include('myapp.urls')),

    #Rutas de la API
    path('', include('myapp.api.urls')),
]
