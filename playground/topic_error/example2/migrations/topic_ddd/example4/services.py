from .const import Code
from .models import Player, Purchase, Reward


class PurchaseService:
    @classmethod
    def purchase(cls, player_id: int, reward_id: int):
        player = Player.get(player_id)
        if not player:
            return {"code": Code.INVALID_PLAYER, "message": "Invalid player."}

        reward = Reward.get(reward_id)
        if not reward:
            return {"code": Code.INVALID_REWARD, "message": "Invalid reward."}

        if player.balance < reward.price:
            return {"code": Code.INSUFFICIENT_BALANCE, "message": "Insufficient balance."}

        player.balance -= reward.price
        player.save()

        _ = Purchase.create(player_id=player_id, reward_id=reward_id)

        return {"code": Code.SUCCESS, "message": "Purchase success."}
