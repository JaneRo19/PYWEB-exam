from rest_framework import serializers
from note_todo.models import NoteToDo, Comment
from datetime import datetime
from django.utils import dateparse


class NoteToDoSerializer(serializers.ModelSerializer):
    """
    Класс, который сериализует модель NoteToDo
    """

    note_status = serializers.SerializerMethodField('get_note_status')

    def get_note_status(self, obj):
        return {
            'value': obj.note_status,
            'display': obj.get_note_status_display()
        }

    class Meta:
        model = NoteToDo
        fields = '__all__'
        read_only_fields = ("author", )

    def to_representation(self, instance):
        """
        Функция, изменяющая представление даты
        :param instance: поля дат: created_at, due_to
        :return: отформатированную дату
        """
        ret = super().to_representation(instance)
        created_at = dateparse.parse_datetime(ret['created_at'])
        ret['created_at'] = created_at.strftime('%d %B %Y %H:%M:%S')

        due_to = dateparse.parse_datetime(ret['due_to'])
        ret['due_to'] = due_to.strftime('%d %B %Y %H:%M:%S')

        return ret


class CommentSerializer(serializers.ModelSerializer):
    """
    Класс, котрый сериализует модель Comment
    """
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, obj):
        return {
            'value': obj.rating,
            'display': obj.get_rating_display()
        }

    class Meta:
        model = Comment
        fields = "__all__"


class NoteToDoDetailSerializer(serializers.ModelSerializer):
    """
    Класс, который сериализует детальную информацию по моделе NoteToDo
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    comment_set = CommentSerializer(many=True,
                                    read_only=True)

    class Meta:
        model = NoteToDo
        fields = (
            'title', 'content', 'created_at', 'due_to', 'importance', 'public',
            'author', 'comment_set'
        )

    def to_representation(self, instance):
        """
        Функция, изменяющая представление даты
        :param instance: поля дат: created_at, due_to
        :return: отформатированную дату
        """
        ret = super().to_representation(instance)
        created_at = dateparse.parse_datetime(ret['created_at'])
        ret['created_at'] = created_at.strftime('%d %B %Y %H:%M:%S')

        due_to = dateparse.parse_datetime(ret['due_to'])
        ret['due_to'] = due_to.strftime('%d %B %Y %H:%M:%S')

        return ret


class QueryParamsStatusFilterSerializer(serializers.Serializer):
    note_status = serializers.ListField(child=serializers.ChoiceField(choices=NoteToDo.NoteStatus.choices), required=False)


class QueryParamsCommentFilterSerializer(serializers.Serializer):
    rating = serializers.ListField(child=serializers.ChoiceField(choices=Comment.Rating.choices), required=False)