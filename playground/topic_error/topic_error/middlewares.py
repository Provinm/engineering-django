import typing as T

from django.http import HttpRequest, HttpResponse, JsonResponse

from . import errors as E


class ErrorMiddleware:
    def __init__(self, get_response: T.Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        resp = self.get_response(request)

        return resp

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
        print(exception)
        new_exception = E.translate_exception(exception)
        return JsonResponse({"msg": new_exception.msg, "code": new_exception.code})
