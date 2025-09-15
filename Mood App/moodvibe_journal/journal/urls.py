from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_mood/', views.submit_mood, name='submit_mood'),
    path('history/', views.history, name='history'),
]