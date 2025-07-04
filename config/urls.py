"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from studio.views import home as studio_home  # Importação absoluta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', studio_home, name='home'),  # Usando o alias direto
    path('studio/', include('studio.urls')),
    #URLs de autenticação do Django (login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]
