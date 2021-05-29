# -*- coding: utf-8 -*-
from django.urls import path, include
from knox.views import LogoutView

from .api.viewsets import UsuarioAPIView, RegistroAPIView, LoginView, ChangePasswordView, ChangeEmailView

urlpatterns = [
	path('', include('knox.urls')),
	path('user', UsuarioAPIView.as_view()),
	path('login', LoginView.as_view()),
	path('register', RegistroAPIView.as_view()),
	path('logout', LogoutView.as_view(), name='knox_logout'),
	path('change_password/<int:pk>', ChangePasswordView.as_view(), name='change_password'),
	path('change_email/<int:pk>', ChangeEmailView.as_view(), name='change_email'),
]
