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
from django.shortcuts import render, redirect
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("/login", permanent=False)),
    path("login", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("dashboard", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("unauthorized", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("404", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("menu", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # Loan Management
    # payments
    path("payments", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("payments/new", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("payments/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # loans
    path("loans", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("loans/add", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("loans/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "loans/<int:id>/amortization/restructure", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))
    ),
    # borrowers
    path("borrowers", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("borrowers/add", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("borrowers/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "borrowers/<int:id>/new-file/<int:subProcessId>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    path(
        "borrowers/<int:id>/new-loan-availment/<int:creditLineId>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    path(
        "borrowers/<int:id>/new-loan-release/<int:loanId>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    path("borrowers/<int:id>/edit", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # processes
    path("processes", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("files", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("files/<str:documentType>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("files/<str:documentType>/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # credit-line
    path("credit-line", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("credit-line/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("amortizations", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("amortizations/maturing", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # checks
    path("checks", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # reports
    path("loan-reports", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "loan-reports/<str:category>/<str:subcategory>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    path("loan-summary", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "loan-summary/<str:category>/<str:subcategory>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    # Settings
    # Committes
    path("committees", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("committees/add", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("committees/<str:officeName>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "committees/<str:officeName>/<int:committee>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    # Terms
    path("terms", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("terms/add", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("terms/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("400", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # Audit Trail
    path("user-logs", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("user-logs/access", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("user-logs/create", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("user-logs/edit", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("user-logs/delete", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    # print
    path("print/<str:state>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("print/borrowers/loans/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "print/borrowers/statement-of-account/<int:id>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    path("print/borrowers/creditlines/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "print/borrowers/payment-history/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))
    ),
    path(
        "print/borrowers/outstanding-obligations/<int:id>",
        ensure_csrf_cookie(TemplateView.as_view(template_name="base.html")),
    ),
    path("print/files/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("print/files/amortization/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "print/loans/amortization-history/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))
    ),
    path("print/loans/payment-history/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path("print/loans/check/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))),
    path(
        "print/loans/statement-of-account/<int:id>", ensure_csrf_cookie(TemplateView.as_view(template_name="base.html"))
    ),
    # App Urls
    path("api/auth/", include("auth.urls")),
    path("api/accounting/", include("accounting.urls"), name="accounting"),
    path("api/borrowers/", include("borrowers.urls"), name="borrowers"),
    path("api/documents/", include("documents.urls"), name="documents"),
    path("api/loans/", include("loans.urls"), name="loans"),
    path("api/payments/", include("payments.urls"), name="payments"),
    path("api/processes/", include("processes.urls"), name="processes"),
    path("api/committees/", include("committees.urls"), name="committees"),
    path("api/notifications/", include("notifications.urls"), name="notifications"),
    path("api/users/", include("users.urls"), name="users"),
    path("api/settings/", include("settings.urls"), name="settings"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
