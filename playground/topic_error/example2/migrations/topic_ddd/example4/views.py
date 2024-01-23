from django.http import HttpRequest, HttpResponse, JsonResponse

from .serializers import Player
from .services import PurchaseService


def purchase(request: HttpRequest) -> HttpResponse:
    player_id = request.POST.get("player_id")
    reward_id = request.POST.get("reward_id")

    # from service
    ret = PurchaseService.purchase(player_id, reward_id)

    return JsonResponse(ret)


def info(request: HttpRequest) -> HttpResponse:
    player_id = request.GET.get("player_id")

    # from serializer
    ret = Player.get_from_id(player_id)

    return JsonResponse(ret.dict())
