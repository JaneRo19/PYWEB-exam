from django.views import View
from django .views.generic import TemplateView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


class IndexView(View):
    """
    Класс, позволяющий использовать специальную статическую форму для входа
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'login/index.html')

    def post(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(request.POST, json_dumps_params={'indent': 4})


class AboutTemplateView(TemplateView):
    """
    Класс, отображающий имя сервера и пользователя
    """
    template_name = 'login/about.html'
