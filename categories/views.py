from django.http import HttpResponse
from django.views import View

# Create your views here.

from django.shortcuts import render


class test(View):
    def get(self, request, *args, **kwargs):
        context = {
            'message': 'Добро пожаловать на мой сайт!'
        }
        return render(request, 'example.html', context)


class MainPage(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("App Admin")