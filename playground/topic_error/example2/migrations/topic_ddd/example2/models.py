from django.db import models

from .const import Code


class PollRecord(models.Model):
    user_email = models.CharField(max_length=20)
    car_brand = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def poll(cls, email: str, brand: str) -> dict:
        if not email:
            return {"code": Code.EMPTY_EMAIL, "message": "Please enter your email."}

        if not brand:
            return {"code": Code.EMPTY_BRAND, "message": "Please enter your car brand."}

        if "@" not in email:
            return {"code": Code.INVALID_EMAIL, "message": "Please enter a valid email."}

        if brand not in ["BMW", "Benz", "Audi"]:
            return {"code": Code.INVALID_BRAND, "message": "Please enter a valid car brand."}

        r = cls.objects.create(user_email=email, car_brand=brand)

        return {"code": Code.SUCCESS, "message": f"Thank you for your poll. id = {r.id}"}
