from django.db import models

from .const import Code


class Player(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)

    @classmethod
    def info(cls, player_id: int) -> dict:
        player = cls.objects.filter(id=player_id)
        if not player.exists():
            return {"code": Code.INVALID_PLAYER, "message": "Invalid player."}

        player = player.first()

        return {
            "code": Code.SUCCESS,
            "data": {"name": player.name, "region": player.region, "balance": player.balance},
        }


class Reward(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    num = models.CharField(max_length=255)
    price = models.IntegerField()


class Purchase(models.Model):
    player_id = models.BigIntegerField()
    reward_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def purchase(cls, player_id: int, reward_id: int) -> dict:
        player = Player.objects.filter(id=player_id)
        if not player.exists():
            return {"code": Code.INVALID_PLAYER, "message": "Invalid player."}

        player = player.first()

        reward = Reward.objects.filter(id=reward_id)
        if not reward.exists():
            return {"code": Code.INVALID_REWARD, "message": "Invalid reward."}

        reward = reward.first()

        if player.balance < reward.price:
            return {"code": Code.INSUFFICIENT_BALANCE, "message": "Insufficient balance."}

        player.balance -= reward.price
        player.save()

        _ = cls.objects.create(player_id=player_id, reward_id=reward_id)

        return {"code": Code.SUCCESS, "message": "Purchase success."}
