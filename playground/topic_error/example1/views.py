import json
import os

from django.core.cache import cache
from django.http import HttpRequest, JsonResponse

from .models import ViewRecord


class Code:
    SUCCESS = 1000
    FILE_NOT_FOUND = 2001
    FILE_NOT_JSON = 2002
    DB_ERROR = 2003
    REDIS_ERROR = 2004


def locate_file(request: HttpRequest) -> JsonResponse:
    file_path = request.GET.get("file_path")

    if not file_path or not os.path.exists(file_path):
        return JsonResponse({"msg": "File not found", "code": Code.FILE_NOT_FOUND})

    with open(file_path, "r") as f:
        content = f.read()
        try:
            json.loads(content)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "File content is not valid json", "code": Code.FILE_NOT_JSON})

    try:
        ViewRecord.objects.create(file_path=file_path)
    except Exception:
        return JsonResponse({"msg": "Database error", "code": Code.DB_ERROR})

    cache_key = f"file_path_{file_path}"
    try:
        if cache.get(cache_key) is None:
            cache.set(cache_key, 0)
        cache.incr(cache_key)
    except Exception:
        return JsonResponse({"msg": "Redis error", "code": Code.REDIS_ERROR})

    return JsonResponse({"msg": "Success", "code": Code.SUCCESS})
