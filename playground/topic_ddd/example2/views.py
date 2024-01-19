from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import PollRecord


# @login_required
def poll(request: HttpRequest) -> HttpResponse:
    email = request.POST.get("user_email")
    brand = request.POST.get("car_brand")

    ret = PollRecord.poll(email, brand)

    return JsonResponse(ret)
