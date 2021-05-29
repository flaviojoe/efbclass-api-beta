from django.urls import path
from .api.viewsets import VideoAulaUpdateView

urlpatterns = [
    path('', VideoAulaUpdateView.as_view())
]
