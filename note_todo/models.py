import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import timedelta


def get_next_day():
    now = datetime.datetime.now()
    return now + timedelta(days=1)


class NoteToDo(models.Model):
    """
    Класс, описывающий состав полей заметки
    """
    class NoteStatus(models.IntegerChoices):
        """
        Класс, описывающий статусы заметки
        """
        ACTIVE = 0, _("Активно")
        EXECUTE = 1, _("Выполнено")
        POSTPONED = 2, _("Отложено")

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(default='', verbose_name='Заметка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    due_to = models.DateTimeField(default=get_next_day, verbose_name='До какого числа исполнить')
    public = models.BooleanField(default=False, verbose_name='Публичная')
    importance = models.BooleanField(default=True, verbose_name='Важно')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    note_status = models.IntegerField(default=NoteStatus.ACTIVE,
                                      choices=NoteStatus.choices,
                                      verbose_name='Статус состояния')

    def __str__(self):
        return f"Заметка {self.title}"

    class Meta:
        verbose_name = _("заметка")
        verbose_name_plural = _("заметки")


class Comment(models.Model):
    """
    Класс, описывающий рейтинг для записей
    """
    class Rating(models.IntegerChoices):
        """
        Класс, устанавливающий велечины рейтинга
        """
        WITHOUT_RATING = 0, _("Без оценки")
        TERRIBLE = 1, _("Ужасно")
        BADLY = 2, _("Плохо")
        FINE = 3, _("Нормально")
        GOOD = 4, _("Хорошо")
        EXCELLENT = 5, _("Отлично")

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    note_todo = models.ForeignKey(NoteToDo, on_delete=models.CASCADE, verbose_name='Заметка')
    rating = models.IntegerField(default=Rating.WITHOUT_RATING,
                                 choices=Rating.choices,
                                 verbose_name='Оценка')

    def __str__(self):
        return f"{self.get_rating_display()} : {self.author}"

    class Meta:
        verbose_name = _("комментарий")
        verbose_name_plural = _("комментарии")
