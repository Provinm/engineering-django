from pydantic import BaseModel

from .models import Player as PlayerModel


class Player(BaseModel):
    name: str
    region: str
    balance: int

    @classmethod
    def get_from_id(self, player_id: int):
        p = PlayerModel.get(player_id)
        if not p:
            return None

        return Player(name=p.name, region=p.region, balance=p.balance)
