from django.urls import path
from .viewsets import VideoAulaUpdateView

urlpatterns = [
    path('', VideoAulaUpdateView.as_view()),
]
