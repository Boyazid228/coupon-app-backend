from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views import View





class MainPage(View):
    def get(self, request, *args, **kwargs):

        return HttpResponse("App Admin")