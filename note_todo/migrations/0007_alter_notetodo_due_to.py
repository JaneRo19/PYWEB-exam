# Generated by Django 4.0.4 on 2022-06-02 08:21

from django.db import migrations, models
import note_todo.models


class Migration(migrations.Migration):

    dependencies = [
        ('note_todo', '0006_alter_comment_author_alter_comment_note_todo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notetodo',
            name='due_to',
            field=models.DateTimeField(default=note_todo.models.get_next_day, verbose_name='До какого числа исполнить'),
        ),
    ]
