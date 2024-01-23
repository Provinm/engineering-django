from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import Player, Purchase


def purchase(request: HttpRequest) -> HttpResponse:
    player_id = request.POST.get("player_id")
    reward_id = request.POST.get("reward_id")

    ret = Purchase.purchase(player_id, reward_id)

    return JsonResponse(ret)


def info(request: HttpRequest) -> HttpResponse:
    player_id = request.GET.get("player_id")

    ret = Player.info(player_id)

    return JsonResponse(ret)
