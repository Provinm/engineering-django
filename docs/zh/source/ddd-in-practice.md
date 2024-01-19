DDD 实践
======

### 综述

本文主要阐述 DDD 设计理念在过往经历过项目的使用经验

- 什么是 DDD
- 什么是充血模式以及其使用经验
- 什么是贫血模式以及其使用经验
- 在实践中对比两种模式并进行简单总结


### DDD

DDD（领域驱动设计）是一种软件开发理念，其目标是通过功能分块分层设计来解决项目的复杂性，相关的文章随手一搜就是一大片，可见

- [极客搜索](https://s.geekbang.org/search/c=0/k=DDD/t=?referrer=InfoQ)
- [wiki](https://en.wikipedia.org/wiki/Domain-driven_design)

以 Django 开发者的视角来看，这些文章都偏理论，本文以个人的开发经验结合实际的代码说明来阐述我是如何理解 DDD 的，在我们的实际开发中，部分项目使用充血模型来编写代码，部分项目使用贫血模型来编写代码，不刻意遵守所谓的 DDD 分层，比如Entity-value/Aggregate/Service/Repository，而是围绕着如何设计是项目代码拥有尽可能的可读性/可维护性。

引入DDD的契机也很巧合，我们当时遇到的问题是如何方便的写测试代码，在一直的实践中，我们把业务代码堆积在视图函数中，其代码可见 [xxx]()，简单示例如下

在django项目的 `views.py` 下

```python

# @login_required
def poll(request: HttpRequest) -> HttpResponse:
    email = request.POST.get("user_email")
    brand = request.POST.get("car_brand")
    if not email:
        return JsonResponse({"code": Code.EMPTY_EMAIL, "message": "Please enter your email."})

    if not brand:
        return JsonResponse({"code": Code.EMPTY_BRAND, "message": "Please enter your car brand."})

    if "@" not in email:
        return JsonResponse({"code": Code.INVALID_EMAIL, "message": "Please enter a valid email."})

    if brand not in ["BMW", "Benz", "Audi"]:
        return JsonResponse({"code": Code.INVALID_BRAND, "message": "Please enter a valid car brand."})

    r = PollRecord.objects.create(user_email=email, car_brand=brand)

    return JsonResponse({"code": Code.SUCCESS, "message": f"Thank you for your poll. id = {r.id}"})



```

以上整个代码的逻辑还是比较清晰，问题是在于如何进行测试，能做到的测试代码如下

```python

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
        self.assertEqual(ret["code"], Code.EMPTY_EMAIL)


```

比较痛苦的是，为了进行测试，我们不得不先构造一个 Request 对象，然后使用 request client 模拟访问视图函数，如果把 `login_required` 打开，还需要想办法绕过登陆，这对测试非常不友好，以至于相当一段时间使用 postman 进行测试。

为了把测试接口转换为测试函数，绕开复杂的测前构造，经过组内讨论，开始引入 DDD 开发理念，它把接口和功能两个模块彻底的分开，并在实践过程中将充血模型带入到代码编写过程中。

### 充血模型

在DDD下继续谈谈充血模式，充血模式的特征是数据和对应的业务逻辑绑定在一起，在业务代码中的分层如下

![Alt text](./截屏2024-01-11 15.14.13.png)

其实际的示例代码可见 []()，简单的示例如下，其中 `views` 代码如下

```python

# @login_required
def poll(request: HttpRequest) -> HttpResponse:
    email = request.POST.get("user_email")
    brand = request.POST.get("car_brand")

    ret = PollRecord.poll(email, brand)

    return JsonResponse(ret)

```

可以看到在将参数解析出来之后，便简单调用了 `PollRecord.poll` 函数，获取结果之后直接进行返回。


```python

class PollRecord(models.Model):
    user_email = models.CharField(max_length=20)
    car_brand = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def poll(cls, email: str, brand: str) -> dict:
        if not email:
            return {"code": Code.EMPTY_EMAIL, "message": "Please enter your email."}

        if not brand:
            return {"code": Code.EMPTY_BRAND, "message": "Please enter your car brand."}

        if "@" not in email:
            return {"code": Code.INVALID_EMAIL, "message": "Please enter a valid email."}

        if brand not in ["BMW", "Benz", "Audi"]:
            return {"code": Code.INVALID_BRAND, "message": "Please enter a valid car brand."}

        r = cls.objects.create(user_email=email, car_brand=brand)

        return {"code": Code.SUCCESS, "message": f"Thank you for your poll. id = {r.id}"}


```


可以看到整个业务逻辑都在 PollRecord model 下，数据的查询等操作可以直接通过 cls 发起，一系列逻辑之后返回字典结果，最后我们看看测试的过程。

```python

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

```


可以看到，进行 `PollRecord.poll` 测试的优点在于不用再去构造 Request 结构体了，直接用简单的 str 就能完成测试。最后可选的补一个 api 测试，api 测试代码的作用仅仅是保证接口的可用性。

以上便是充血模式在我们项目中的基本应用。

接下来说一个跟领域设计相关的例子，假定我们有三个实体

- Player
- Reward
- Purchase

然后有两个接口

- api/player/info(玩家登陆并获取信息)
- api/player/purchase(玩家购买指定物品)

在实际的代码中，会怎么来安排以上的代码呢


`views.py`


```python

def purchase(request: HttpRequest) -> HttpResponse:
    player_id = request.POST.get("player_id")
    reward_id = request.POST.get("reward_id")

    ret = Purchase.purchase(player_id, reward_id)

    return JsonResponse(ret)


def info(request: HttpRequest) -> HttpResponse:
    player_id = request.GET.get("player_id")

    ret = Player.info(player_id)

    return JsonResponse(ret)


```


`models.py`



```python


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


```

测试代码就不放了，参考上面一个例子。

可以看到我是将 purchase 方法放在 Purchase 类下，而不是 Player 下，从语义上讲 `Player.purchase` 比起 `Purchase.purchase` 更好理解，但我们仍然坚持把 purchase 放在 Purchase model 下，这一是涉及到对领域的理解，我们认为 purchase 方法产生的结果数据落在 Purchase 表下，而不是 Player 表下。另外如果把跟 Player 相关的所有方法均放到 Player 下会造成 Player 类下代码太长，其他类代码又太少的头重脚轻的情况。

这就是我们对DDD充血模式理解的最佳实践，我们将此模式应用到公司内部面向外部用户的业务中，因为在这些业务中，单个项目的接口数量较少，业务逻辑相对不复杂，这个开发体验是相当不错的。

但随着组里的业务扩展到公司内部的一些平台项目中，此模式遇到了一些问题，在平台类的项目中，业务逻辑相对来复杂，如果是要用充血模式的话，会造成一个类可能有上千行的业务逻辑，这些业务逻辑没有办法按领域进行划分，这带来了可读性的问题，那么一次次的实践中，我们决定就是在平台类的项目，就是业务逻辑重的项目里面去使用贫血模式。


### 贫血模式

相比于刚刚的充血模式，贫血模式是将业务逻辑从实体类上剥离下来，单独成为service，实体类仅简单提供对外的数据控制方法，用一个图说明贫血模式下，文件结构和功能分层。

![Alt text](./截屏2024-01-11 17.37.30.png)


解释一下此图，贫血模式在项目代码里面分为以下几层，第一层就是视图函数，这是所有对外的接口，然后视图函数这一层再往下就是有可能到两个地方，第一个地方就是service层，是实际的去写这些业务逻辑的地方。

另一个是序列化层，在做中台的项目的时候，常常对某个model的需求只有增删改查，使用 serializer 来承接这一部分简单的工作，类似于 [django-restful-framework]，在文章 [xxx] 说明了为什么我们不用 restful。

再往下去到service层，到了service层之后再往下也有可能到两个地方，第一个地方就是序列化层，一些时候序列化层提供的默认函数经过一些简单的改造，就能被service层使用，另外一方到 Model层，model下包含一些比较简单的一些函数，比如 get/filter 等，那么这种分层就是解决了我们在中平台业内的业务中的一个使用。

下面我用实际的代码来解释一下，完整代码见 [xxx]()，简单代码见

`views.py`


```python

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

```

`service.py`

```python

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

```

在 service 层进行实际的业务逻辑编写。

`serializer.py`

```python

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


```

> 实际的业务代码中，serializer 会比较复杂，有更多的函数，比如 `create`/`update`/`delete` 等，这里仅仅是为了说明贫血模式下的代码分层。

`models.py`

```python


class Player(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)

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

    @classmethod
    def create(cls, player_id: int, reward_id: int):
        record = cls.objects.create(player_id=player_id, reward_id=reward_id)
        return record

```


models 下的函数全部围绕数据操作，比如 get/create/update/delete 等。


可以看到，贫血模式下，代码分层更加清晰，views/serializer/service/model 之间的关系也更加清晰，这样的代码在中台类的项目中，可读性和可维护性都要好很多。

### 配套代码使用

本项目解释代码在 []()

使用流程如下

```sh

docker-compose up -d 
docker-compose exec web bash 

cd topic_ddd
make migrate
make test

# run server
# make run

```

### 总结


在看完整个代码之后，当去结合DDD准则来看时，其中的一些概念和实际的代码对不上，比如在我上述的项目中，Entity 可以对应到 Model 层，但 Repository 是没有代码对应的，我是把 Entity 和 Repository 放到了一起。想提这一点是避免教条主义，一切要切合实际的业务需求进行，在一个中小项目中不分编程语言，不分web框架，严格按照 DDD 所有的原则写代码，最后一定会出问题。

我所在的组里，充血模式和贫血模式都在使用，并且用在了两种不同的业务里面。充血模式用在了简单相对业务逻辑相对简单，然后贫血模式是用在了就是平台类的业务中，目前运行良好。

总之，不能想着用一种银弹去适应所有的业务，这个是很关键的，只能在大的方向上以

- 代码可读性要强
- 代码可维护性要好
- 代码可扩展性要高
- 开发体验要好

等等原则来指导业务代码编写。

