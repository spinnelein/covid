"""covid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import settings
from . import views
from .views import *
from .forms import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',QuizWizard.as_view(FORMS, condition_dict={
        'symptoms':showsymptoms,
        'currentsymptoms':asymptomatic,
        'dyspnea':asymptomatic,
        'o2':showo2,
        'o2reading':showo2reading,
        'lightheadedness':asymptomatic,
        'acuity':asymptomatic,
        'chestpain':asymptomatic,
        'clinic':asymptomatic,
        'constantexposure':showongoing
    }))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
