from django.http import HttpRequest, HttpResponse, JsonResponse

from .const import Code
from .models import PollRecord


# @login_required
def poll(request: HttpRequest) -> HttpResponse:
    email = request.POST.get("user_email")
    brand = request.POST.get("car_brand")
    if not email:
        return JsonResponse({"code": Code.EMPTY_EMAIL, "message": "Please enter your email."})

    if not brand:
        return JsonResponse({"code": Code.EMPTY_BRAND, "message": "Please enter your car brand."})

    if "@" not in email:
        return JsonResponse({"code": Code.INVALID_EMAIL, "message": "Please enter a valid email."})

    if brand not in ["BMW", "Benz", "Audi"]:
        return JsonResponse({"code": Code.INVALID_BRAND, "message": "Please enter a valid car brand."})

    r = PollRecord.objects.create(user_email=email, car_brand=brand)

    return JsonResponse({"code": Code.SUCCESS, "message": f"Thank you for your poll. id = {r.id}"})
