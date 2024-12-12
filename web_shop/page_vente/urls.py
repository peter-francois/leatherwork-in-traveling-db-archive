from django.urls import path
from . import views

app_name = 'boutique'

urlpatterns = [
    path('', views.index, name="index"),
    path('macrames/', views.macrames, name="macrames"),
]