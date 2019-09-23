"""python_exam_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from python_exam_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_register),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.show_all_trips),
    path('add_trip', views.add_trip),
    path('create_trip', views.create_trip),
    path('logout', views.logout),
    path('trip/<int:number>', views.trip_info),
    path('join_trip/<int:number>', views.join_trip)
]
