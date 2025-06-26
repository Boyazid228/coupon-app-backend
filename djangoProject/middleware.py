# yourapp/middleware.py
from django.http import HttpResponseForbidden


class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/login/' or request.path == '/admin/logout/':
            return self.get_response(request)

        if request.path.startswith('/admin/') and not (request.user.is_authenticated and request.user.is_superuser):
            return HttpResponseForbidden("Access Denied")

        return self.get_response(request)