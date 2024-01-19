from django.test import TestCase
from example2.const import Code
from example2.models import PollRecord


# Create your tests here.
class TestPoll(TestCase):
    def setUp(self) -> None:
        PollRecord.objects.all().delete()

    def test_poll(self):
        # test case 1
        ret = PollRecord.poll("user1@qq.com", "BMW")
        self.assertEqual(ret["code"], Code.SUCCESS)

        # case 2
        ret = PollRecord.poll("", "BMW")
        self.assertEqual(ret["code"], Code.EMPTY_EMAIL)

        # case 3
        ret = PollRecord.poll("user1@qq.com", "")
        self.assertEqual(ret["code"], Code.EMPTY_BRAND)

    def test_api(self):
        resp = self.client.post("/api/example2/poll", {"user_email": "user1@qq.com", "car_brand": "BMW"})
        ret = resp.json()
        self.assertEqual(ret["code"], Code.SUCCESS)
