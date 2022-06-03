from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.IndexView.as_view()),
    path('about/', views.AboutTemplateView.as_view()),
]
