from django.test import TestCase
from example3 import models as M


class TestPurchase(TestCase):
    def setUp(self) -> None:
        M.Player.objects.all().delete()
        M.Purchase.objects.all().delete()
        M.Reward.objects.all().delete()

        self.r1 = M.Reward.objects.create(name="r1", color="red", num="1", price=100)
        self.r2 = M.Reward.objects.create(name="r2", color="blue", num="2", price=200)
        self.p1 = M.Player.objects.create(name="p1", region="r1", balance=1000)
        self.p2 = M.Player.objects.create(name="p2", region="r2", balance=20)

    def test_purchase(self):
        ret = M.Purchase.purchase(self.p1.id, self.r1.id)
        self.assertEqual(ret["code"], M.Code.SUCCESS)

        ret = M.Purchase.purchase(self.p1.id + 100, self.r2.id)
        self.assertEqual(ret["code"], M.Code.INVALID_PLAYER)

        ret = M.Purchase.purchase(self.p2.id, self.r1.id + 100)
        self.assertEqual(ret["code"], M.Code.INVALID_REWARD)

        ret = M.Purchase.purchase(self.p2.id, self.r2.id)
        self.assertEqual(ret["code"], M.Code.INSUFFICIENT_BALANCE)

    def test_info(self):
        ret = M.Player.info(self.p1.id)
        self.assertEqual(ret["code"], M.Code.SUCCESS)

        ret = M.Player.info(self.p1.id + 100)
        self.assertEqual(ret["code"], M.Code.INVALID_PLAYER)
