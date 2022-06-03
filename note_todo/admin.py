from django.contrib import admin
from .models import NoteToDo, Comment


@admin.register(NoteToDo)
class NoteToDoAdmin(admin.ModelAdmin):
    """
    Класс, регистрирующий модель в админке, с настроеннфми полями
    """
    list_display = ('title', 'note_status', 'importance', 'public', 'created_at', 'due_to', 'author')

    fields = (('title', 'public', 'importance'), 'note_status', 'content', 'created_at', 'due_to', 'author')
    readonly_fields = ('created_at',)

    search_fields = ('title', 'content', 'due_to')
    list_filter = ('public', 'author', 'importance')
    ordering = ('-created_at', 'importance')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Класс, регистрирующий модель комментариев в админке с настроенными полями
    """
    list_display = ('author', 'note_todo', 'rating')
