from rest_framework.views import APIView
from note_todo.models import NoteToDo, Comment
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from . import serializers
from . import filters
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models.functions import Trunc
from django.db.models import DateField


class NoteToDoListCreateAPIView(APIView):
    """
    Класс, возвращающий get и post запросы модели NoteToDo
    """
    def get(self, request: Request) -> Response:
        """
        Функция, возвращающая get запрос модели NoteToDo
        :param request: запрос
        :return: список заметок
        """
        objects = NoteToDo.objects.all()
        serializer = serializers.NoteToDoSerializer(instance=objects, many=True)

        return Response(data=serializer.data)

    def post(self, request: Request) -> Response:
        """
        Функция, возвращающая post запрос модели NoteToDo
        :param request: заметка пользователя
        :return: добавление в базу данных заметки
        """
        serializer = serializers.NoteToDoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class NoteToDoDetailAPIView(APIView):
    """
    Класс, предоставляющий детальную информацию по каждой заметке
    """
    def get(self, request: Request, pk) -> Response:
        """
        Функция, которая возвращает get запрос модели NoteToDo по конкретной записи
        :param request: запрос
        :param pk: id записи
        :return: заметку по ее id
        """
        note = get_object_or_404(NoteToDo, pk=pk)
        serializer = serializers.NoteToDoDetailSerializer(instance=note)

        return Response(serializer.data)

    def put(self, request: Request, pk) -> Response:
        """
        Функция, которая позволяет автору изменить любое поле заметки
        :param request: запрос с изменениями
        :param pk: id заметки
        :return: измененную заметку по ее id
        """
        note = get_object_or_404(NoteToDo, pk=pk)
        serializer = serializers.NoteToDoDetailSerializer(instance=note,
                                                          data=request.data,
                                                          partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        if note.author != request.user:
            return Response(
                data='Вы не можете менять заметку. Ее может изменить только автор',
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(author=request.user)

        return Response(serializer.data)

    def patch(self, request: Request, pk) -> Response:
        """
        Функция, которая позволяет автору изменить любое поле заметки,
        но с обязательным изменением заголовка
        :param request: запрос с изменениями. Поле title обязательно
        :param pk: id заметки
        :return: измененную заметку по ее id
        """
        note = get_object_or_404(NoteToDo, pk=pk)
        serializer = serializers.NoteToDoDetailSerializer(instance=note,
                                                          data=request.data,
                                                          partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if note.author != request.user:
            return Response(
                data='Вы не можете изменить заметку. Заметку может менять только автор',
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(author=request.user)

        return Response(serializer.data)

    def delete(self, request: Request, pk) -> Response:
        """
        Функция, которая позволяет автору удалить его запись
        :param request: запрос
        :param pk: id заметки
        :return: сообщение об удалении заметки, если ее удалил автор
        """
        note = get_object_or_404(NoteToDo, pk=pk)

        if note.author != request.user:
            return Response(
                data='Вы не можете удалить заметку. Заметку может удалять только автор',
                status=status.HTTP_403_FORBIDDEN
            )
        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicNoteToDoListAPIView(ListAPIView):
    """
    Класс, который показывает только опубликованные записи
    """
    queryset = NoteToDo.objects.all()
    serializer_class = serializers.NoteToDoDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(public=True)


class NoteToDoFilterListAPIView(ListAPIView):
    """
    Класс, который фильтрует данные по важности и по публичности.
    Необходимо задать параметр ?importance=True, ?importance=False, ?public=True, ?public=False
    или комбинацию этих фильтров
    """
    queryset = NoteToDo.objects.all()
    serializer_class = serializers.NoteToDoSerializer

    def filter_queryset(self, queryset):
        queryset = filters.importance_filter(queryset, importance=self.request.query_params.get('importance'))
        queryset = filters.public_filter(queryset, public=self.request.query_params.get("public"))

        return queryset


class NoteToDoSortListAPIView(ListAPIView):
    """
    Класс, который сотрирует заметки сначала по дате, и в разрезе дат по важности
    """
    queryset = NoteToDo.objects.all()
    serializer_class = serializers.NoteToDoSerializer

    def get_queryset(self):
        queryset = self.queryset.order_by(Trunc('created_at', 'day', output_field=DateField()).desc(),
                                          '-importance')

        return queryset


class NoteToDoFilterStatusListAPIView(ListAPIView):
    """
    Класс, который позволяет вывести отфильтрованные данные по статусам: Активно, Выполнено,
    Отложено. Как по одному, так и любая их комбинация.
    Запрос должен содержать: ?note_status=0, ?note_status=1, ?note_status=2
    """
    queryset = NoteToDo.objects.all()
    serializer_class = serializers.NoteToDoSerializer

    def filter_queryset(self, queryset):
        query_params = serializers.QueryParamsStatusFilterSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        list_status = query_params.data.get('note_status')
        if list_status:
            queryset = queryset.filter(note_status__in=query_params.data['note_status'])

        return queryset


class NoteToDoFilterCommentListAPIView(ListAPIView):
    """
    Класс, который позволяет вывести отфильтрованные данные по рейтингу заметок
    Как по одному, так и любая их комбинация.
    Запрос должен содержать: ?rating=0, ?rating=1, ?rating=2, ?rating=3, ?rating=4, ?rating=5
    """
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def filter_queryset(self, queryset):
        query_params = serializers.QueryParamsCommentFilterSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        list_rating = query_params.data.get('rating')
        if list_rating:
            queryset = queryset.filter(rating__in=query_params.data['rating'])

        return queryset
