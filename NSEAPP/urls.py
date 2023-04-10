"""stockprediction URL Configuration

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
from django.urls import path,include
from . import views
from NSEAPP.views import *
urlpatterns = [
    path('home/',views.homeview,name='homeview'),
    path('base/', views.baseview, name='baseview'),
    path('register/',views.registerview),
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.userlogout,name='logout'),
    path('marketview/',views.marketview,name='marketview'),
    path('marketlight/',views.marketlight,name='marketlight'),
    path('fetch-stock/', views.stock_fetch, name='stock_fetch')
   

]
