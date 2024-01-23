import json
import os

from django.core.cache import cache
from django.http import HttpRequest, JsonResponse
from topic_error import errors as E

from .models import ViewRecord


def locate_file(request: HttpRequest) -> JsonResponse:
    file_path = request.GET.get("file_path")

    if not file_path or not os.path.exists(file_path):
        raise E.FileNotFound()

    with open(file_path, "r") as f:
        content = f.read()
        json.loads(content)

    ViewRecord.objects.create(file_path=file_path)

    cache_key = f"file_path_{file_path}"
    if cache.get(cache_key) is None:
        cache.set(cache_key, 0)
    cache.incr(cache_key)

    return JsonResponse({"msg": "Success", "code": 1000})
