import json

from django.db import utils as django_db_utils


class BaseError(Exception):
    msg = "Base error"
    code = 1000


class FileNotFound(BaseError):
    msg = "File not found"
    code = 2001


class FileNotJson(BaseError):
    msg = "File content is not valid json"
    code = 2002


class DbError(BaseError):
    msg = "Database error"
    code = 2003


class RedisError(BaseError):
    msg = "Redis error"
    code = 2004


def translate_exception(exception: Exception) -> BaseError:
    if isinstance(exception, django_db_utils.Error):
        return DbError()
    elif isinstance(exception, RedisError):
        return RedisError()
    elif isinstance(exception, BaseError):
        return exception
    elif isinstance(exception, FileNotFoundError):
        return FileNotFound()
    elif isinstance(exception, json.JSONDecodeError):
        return FileNotJson()
    else:
        return BaseError()
