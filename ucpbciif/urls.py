"""ucpbciif URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView 
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render,redirect
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),

    path('a', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path('', lambda request: redirect('/login', permanent=False)),
    path('login', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path('dashboard', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    
    #loans
    path('loans', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path('loans/add', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),

    #borrowers
    path('borrowers', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path('borrowers/add', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path('borrowers/<int:id>', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path('borrowers/<int:id>/edit', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),

    path('400', ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # App Urls
    path('api/auth/',include('auth.urls')),
    path('api/borrowers/',include('borrowers.urls'),name='borrowers'),
    path('api/loans/',include('loans.urls'),name='loans'),
    path('api/users/',include('users.urls'),name='users'),
    path('api/settings/',include('settings.urls'),name='settings'), 
]
