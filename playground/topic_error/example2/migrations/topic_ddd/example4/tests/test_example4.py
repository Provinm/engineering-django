from django.test import TestCase
from example4 import models as M
from example4 import services as S
from example4.const import Code
from example4.serializers import Player


class TestPurchase(TestCase):
    def setUp(self) -> None:
        M.Player.objects.all().delete()
        M.Reward.objects.all().delete()
        M.Purchase.objects.all().delete()

        self.r1 = M.Reward.objects.create(name="r1", color="red", num="1", price=100)
        self.r2 = M.Reward.objects.create(name="r2", color="blue", num="2", price=200)
        self.p1 = M.Player.objects.create(name="p1", region="r1", balance=1000)
        self.p2 = M.Player.objects.create(name="p2", region="r2", balance=20)

    def test_service(self):
        ret = S.PurchaseService.purchase(self.p1.id, self.r1.id)
        self.assertEqual(ret["code"], Code.SUCCESS)

        p1 = M.Player.objects.get(id=self.p1.id)
        self.assertEqual(p1.balance, 900)

        exised_record = M.Purchase.objects.filter(player_id=self.p1.id, reward_id=self.r1.id)
        self.assertTrue(exised_record.exists())

        ret = S.PurchaseService.purchase(self.p1.id + 100, self.r2.id)
        self.assertEqual(ret["code"], Code.INVALID_PLAYER)

        ret = S.PurchaseService.purchase(self.p2.id, self.r1.id + 100)
        self.assertEqual(ret["code"], Code.INVALID_REWARD)

        ret = S.PurchaseService.purchase(self.p2.id, self.r2.id)
        self.assertEqual(ret["code"], Code.INSUFFICIENT_BALANCE)

    def test_player_model(self):
        ret = M.Player.get(self.p1.id)
        self.assertEqual(ret.id, self.p1.id)

        ret = M.Player.get(self.p1.id + 100)
        self.assertIsNone(ret)

    def test_purchase_model(self):
        record = M.Purchase.create(self.p1.id, self.r2.id)
        self.assertEqual(record.player_id, self.p1.id)
        self.assertEqual(record.reward_id, self.r2.id)

    def test_reward_model(self):
        ret = M.Reward.get(self.r1.id)
        self.assertEqual(ret.id, self.r1.id)

        ret = M.Reward.get(self.r1.id + 100)
        self.assertIsNone(ret)

    def test_serializer(self):
        ret = Player.get_from_id(self.p1.id)
        self.assertEqual(ret.name, self.p1.name)
        self.assertEqual(ret.region, self.p1.region)
        self.assertEqual(ret.balance, self.p1.balance)
