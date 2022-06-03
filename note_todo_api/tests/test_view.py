import unittest
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from note_todo.models import NoteToDo


class TestNoteToDoListCreateAPIView(APITestCase):
    """
    Класс, в котором тестируются созданные записи
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test_user")

    def test_empty_list_objects(self):
        """
        Функция теститования пустого запроса
        """
        url = "/api/note/"
        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_list_object(self):
        """
        Функция тестирования наличия объекта
        :return:
        """
        url = "/api/note/"
        test_user = User.objects.get(username="test_user")

        NoteToDo.objects.create(title="Test_title", author=test_user)

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        self.assertEqual(1, len(response_data))

    @unittest.skip("Еще не доработала")
    def test_create_object(self):
        """
        Функция тестирования создания объекта
        :return:
        """
        url = "/api/note/"
        new_title = "test_title"

        data = {
            "title": new_title
        }
        resp = self.client.post(url, data=data, username='test_user')

        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        self.assertTrue(NoteToDo.objects.exists(title=new_title))


class TestNoteToDoDetailAPIView(APITestCase):
    """
    Тестирование детальной информации о записях
    """
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(username="test_user")
        NoteToDo.objects.create(title="Test_title", author=test_user)

    @unittest.skip("Ошибка 301")
    def test_retrieve_objects(self):
        note_pk = 6
        url = f"/api/note/{note_pk}"
        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        expected_data = {
              "title": "Test_title",
              "author": 1,
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_does_not_exists_object(self):
        """
        Функция тестирования запроса несуществующего pk
        """
        does_not_exist_pk = "12312341241234"
        url = f"/note/{does_not_exist_pk}"

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, resp.status_code)


class TestNoteToDoFilterCommentListAPIView(APITestCase):
    """
    Тестирование класса фильтрации комментариев
    """
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(username="test_user")
        NoteToDo.objects.create(title="Test_title", author=test_user)

    def test_does_not_exists_rating(self):
        """
        Функция тестирования несуществующего значения рейтинга
        """
        does_not_exists_rating = 100
        url = f'/api/note/filter/comment/?rating={does_not_exists_rating}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)

    def test_valid_rating(self):
        """
        Функция тестирования существующего и валидного значения рейтинга
        """
        exists_rating = 2
        url = f'/api/note/filter/comment/?rating={exists_rating}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_valid_double_rating(self):
        """
        Функция тестирования двух существующих и валидных значений рейтингов
        """
        exists_rating_1 = 1
        exists_rating_2 = 5
        url = f'/api/note/filter/comment/?rating={exists_rating_1}&rating={exists_rating_2}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_str_rating(self):
        """
        Функция тестирования невалидного значения рейтинга
        """
        str_rating = 'small'
        url = f'/api/note/filter/comment/?rating={str_rating}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)


class TestNoteToDoFilterStatusListAPIView(APITestCase):
    """
    Тестирование класса статуса заметки
    """
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(username="test_user")
        NoteToDo.objects.create(title="Test_title", author=test_user)

    def test_does_not_exists_status(self):
        """
        Функция тестирования несуществующего значения статуса, у нас 0, 1, 2
        """
        does_not_exists_status = 100
        url = f'/api/note/filter/status/?note_status={does_not_exists_status}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)

    def test_valid_status(self):
        """
        Функция тестирования существующего и валидного значения статуса
        """
        exists_status = 1
        url = f'/api/note/filter/status/?note_status={exists_status}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_valid_double_status(self):
        """
        Функция тестирования двух существующих и валидных значений статусов
        """
        exists_status_1 = 1
        exists_status_2 = 0
        url = f'/api/note/filter/status/?note_status={exists_status_1}&note_status={exists_status_2}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_str_status(self):
        """
        Функция тестирования невалидного значения статуса
        """
        str_status = 'big'
        url = f'/api/note/filter/status/?note_status={str_status}'

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
