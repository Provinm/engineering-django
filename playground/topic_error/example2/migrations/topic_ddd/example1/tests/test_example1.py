from django.test import TestCase
from example1.const import Code


class TestPoll(TestCase):
    def test_poll(self):
        # test case 1
        resp = self.client.post(
            "/api/example1/poll",
            {"user_email": "user1@qq.com", "car_brand": "BMW"},
        )
        ret = resp.json()
        self.assertEqual(ret["code"], Code.SUCCESS)

        # case 2
        resp = self.client.post(
            "/api/example1/poll",
            {"user_email": "", "car_brand": "BMW"},
        )
        ret = resp.json()
        self.assertEqual(ret["code"], Code.EMPTY_EMAIL)

        # case 3
        resp = self.client.post(
            "/api/example1/poll",
            {"user_email": "user1@qq.com", "car_brand": ""},
        )
        ret = resp.json()
        self.assertEqual(ret["code"], Code.EMPTY_BRAND)
