"""SAWA_SYS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from Aplicaciones.Home.views import *
from Aplicaciones.Login.views import *
from Aplicaciones.Login.forms import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from  Aplicaciones.Home.views import page_not_found404

urlpatterns = [
    #path('', Home.as_view(),name='home'),
    #path('login/', include('Aplicaciones.Login.urls')),
    #path('', include('Aplicaciones.Login.urls')),
    path('', include('Aplicaciones.Login.urls')),
     # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('Compra/', include('Aplicaciones.Compra.urls')),
    path('Producto/', include('Aplicaciones.Producto.urls')),
    path('Reporte/', include('Aplicaciones.Reporte.urls')),
    path('Venta/', include('Aplicaciones.Venta.urls')),
    path('Caja/', include('Aplicaciones.Caja.urls')),
    path('user/', include('Aplicaciones.User.urls')),
]
handler404 = page_not_found404
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

