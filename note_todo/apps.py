from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class NoteTodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'note_todo'

    verbose_name = _("Заметки")
