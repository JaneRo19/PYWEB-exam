from django.urls import path
from . import views

urlpatterns = [
    path('note/', views.NoteToDoListCreateAPIView.as_view()),
    path('note/<int:pk>/', views.NoteToDoDetailAPIView.as_view()),
    path('note/filter/', views.NoteToDoFilterListAPIView.as_view()),
    path('note/filter/status/', views.NoteToDoFilterStatusListAPIView.as_view()),
    path('note/sort/', views.NoteToDoSortListAPIView.as_view()),
    path('note/filter/comment/', views.NoteToDoFilterCommentListAPIView.as_view()),
    path('note/public/', views.PublicNoteToDoListAPIView.as_view()),
]
