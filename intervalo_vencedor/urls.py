from django.urls import path
from .views import maior_intervalo

urlpatterns = [
    path('intervalo/', maior_intervalo, name='maior_intervalo'),
]