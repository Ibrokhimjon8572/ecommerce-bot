"""ecommercebot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from django.views.generic.base import RedirectView

from django.conf.urls.static import static
from django.conf import settings
from telegram.views import index, set_webhook
from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Fayz Baraka Metal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/', index),
    path('set-webhook/', set_webhook),
    path('', RedirectView.as_view(url='/admin')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
