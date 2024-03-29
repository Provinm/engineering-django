from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)

    class Meta:
        db_table = "topic_ddd_example4_player"

    @classmethod
    def get(cls, player_id: int):
        player = cls.objects.filter(id=player_id)
        if not player.exists():
            return None

        return player.first()


class Reward(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    num = models.CharField(max_length=255)
    price = models.IntegerField()

    class Meta:
        db_table = "topic_ddd_example4_reward"

    @classmethod
    def get(cls, reward_id: int):
        reward = cls.objects.filter(id=reward_id)
        if not reward.exists():
            return None

        return reward.first()


class Purchase(models.Model):
    player_id = models.BigIntegerField()
    reward_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "topic_ddd_example4_purchase"

    @classmethod
    def create(cls, player_id: int, reward_id: int):
        record = cls.objects.create(player_id=player_id, reward_id=reward_id)
        return record
