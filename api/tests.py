import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Category,
    Subcategory,
    Product,
    ProductImage,
    ProductSale,
    Review,
    Tag,
    Basket,
    Order,
    OrderItem,
)


class CategoriesListViewTestCase(TestCase):
    """
    TestCase for CategoriesListView
    """
    @classmethod
    def setUpClass(cls):
        cls.category = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory = Subcategory.objects.create(
            id=123001,
            category=cls.category,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )

    @classmethod
    def tearDownClass(cls):
        cls.category.delete()
        cls.subcategory.delete()

    def test_get(self):
        response = self.client.get(reverse("api:categories"))
        data = response.data[0]
        subcategories = data["subcategories"][0]
        subcategory_image = subcategories["image"]
        image = data["image"]
        self.assertContains(response, data["id"])
        self.assertContains(response, data["title"])
        self.assertContains(response, subcategories["id"])
        self.assertContains(response, subcategories["title"])
        self.assertContains(response, subcategory_image["src"])
        self.assertContains(response, subcategory_image["alt"])
        self.assertContains(response, image["src"])
        self.assertContains(response, image["alt"])


class SaleProductsListViewTestCase(TestCase):
    """
    TestCase for SaleProductsListView
    """
    @classmethod
    def setUpClass(cls):
        cls.category = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory = Subcategory.objects.create(
            id=123001,
            category=cls.category,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )

        cls.product = Product.objects.create(
            category=cls.subcategory,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=False,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_sale = ProductSale.objects.create(
            product=cls.product,
            salePrice=200.67,
            dateFrom=datetime.date.today(),
            dateTo=datetime.date.today()

        )

    @classmethod
    def tearDownClass(cls):
        cls.product_sale.delete()
        cls.product.delete()
        cls.subcategory.delete()
        cls.category.delete()

    def test_get(self):
        response = self.client.get(reverse("api:sales"))
        data = response.data["items"][0]
        self.assertContains(response, data["id"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["salePrice"])
        self.assertContains(response, data["dateFrom"])
        self.assertContains(response, data["dateTo"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["images"])
        self.assertContains(response, response.data["currentPage"])
        self.assertContains(response, response.data["lastPage"])


class CatalogListViewTsetCase(TestCase):
    """
    TestCase for CatalogListView
    """
    @classmethod
    def setUpClass(cls):
        cls.category = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory = Subcategory.objects.create(
            id=123001,
            category=cls.category,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )

        cls.product_tag = Tag.objects.create(
            name="Gaming",
        )
        cls.product_tag.category.set([cls.subcategory])

        cls.product = Product.objects.create(
            category=cls.subcategory,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=False,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product,
            src="/3.png",
            alt="Image alt string"
        )
        cls.user = User.objects.create_user("test", "test@test.test", "!@#$%67890qwerty")

        cls.product_review = Review.objects.create(
            product=cls.product,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )

    @classmethod
    def tearDownClass(cls):
        cls.product_review.delete()
        cls.product_image.delete()
        cls.product.delete()
        cls.subcategory.delete()
        cls.category.delete()
        cls.user.delete()

    def test_get(self):
        response = self.client.get(reverse("api:catalog"))
        data = response.data["items"][0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"])
        self.assertContains(response, data["category"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["count"])
        self.assertContains(response, data["date"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["description"])
        self.assertContains(response, str(data["freeDelivery"]).lower())
        self.assertContains(response, images["src"])
        self.assertContains(response, images["alt"])
        self.assertContains(response, tags["id"])
        self.assertContains(response, tags["name"])
        self.assertContains(response, data["reviews"])
        self.assertContains(response, data["rating"])
        self.assertContains(response, response.data["currentPage"])
        self.assertContains(response, response.data["lastPage"])


class PopularProductsListViewTsetCase(TestCase):
    """
    TestCase for PopularProductsListView
    """
    @classmethod
    def setUpClass(cls):
        cls.category = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory = Subcategory.objects.create(
            id=123001,
            category=cls.category,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )

        cls.product_tag = Tag.objects.create(
            name="Gaming",
        )
        cls.product_tag.category.set([cls.subcategory])

        cls.product_one = Product.objects.create(
            category=cls.subcategory,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=True,
            available=True,
        )
        cls.product_one.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_one,
            src="/3.png",
            alt="Image alt string"
        )
        cls.user = User.objects.create_user("test", "test@test.test", "!@#$%67890qwerty")

        cls.product_review = Review.objects.create(
            product=cls.product_one,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_two = Product.objects.create(
            category=cls.subcategory,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_two.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_two,
            src="/3.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_two,
            author=cls.user,
            rate=3,
            text="review text",
            date=datetime.date.today()
        )

    @classmethod
    def tearDownClass(cls):
        cls.product_review.delete()
        cls.product_image.delete()
        cls.product_one.delete()
        cls.product_two.delete()
        cls.subcategory.delete()
        cls.category.delete()
        cls.user.delete()

    def test_get(self):
        response = self.client.get(reverse("api:popular"))
        data = response.data[0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"])
        self.assertEquals(data["id"], self.product_one.id)
        self.assertNotEquals(data["id"], 2)
        self.assertContains(response, data["category"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["count"])
        self.assertContains(response, data["date"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["description"])
        self.assertContains(response, str(data["freeDelivery"]).lower())
        self.assertContains(response, images["src"])
        self.assertContains(response, images["alt"])
        self.assertContains(response, tags["id"])
        self.assertContains(response, tags["name"])
        self.assertContains(response, data["reviews"])
        self.assertContains(response, data["rating"])


class LimitedProductsListViewTsetCase(TestCase):
    """
    TestCase for LimitedProductsListView
    """
    @classmethod
    def setUpClass(cls):
        cls.category = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory = Subcategory.objects.create(
            id=123001,
            category=cls.category,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )

        cls.product_tag = Tag.objects.create(
            name="Gaming",
        )
        cls.product_tag.category.set([cls.subcategory])

        cls.product_one = Product.objects.create(
            category=cls.subcategory,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=True,
            available=True,
        )
        cls.product_one.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_one,
            src="/3.png",
            alt="Image alt string"
        )
        cls.user = User.objects.create_user("test", "test@test.test", "!@#$%67890qwerty")

        cls.product_review = Review.objects.create(
            product=cls.product_one,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_two = Product.objects.create(
            category=cls.subcategory,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_two.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_two,
            src="/3.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_two,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )

    @classmethod
    def tearDownClass(cls):
        cls.product_review.delete()
        cls.product_image.delete()
        cls.product_one.delete()
        cls.product_two.delete()
        cls.subcategory.delete()
        cls.category.delete()
        cls.user.delete()

    def test_get(self):
        response = self.client.get(reverse("api:limited"))
        data = response.data[0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"])
        self.assertEquals(data["id"], self.product_one.id)
        self.assertNotEquals(data["id"], 2)
        self.assertContains(response, data["category"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["count"])
        self.assertContains(response, data["date"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["description"])
        self.assertContains(response, str(data["freeDelivery"]).lower())
        self.assertContains(response, images["src"])
        self.assertContains(response, images["alt"])
        self.assertContains(response, tags["id"])
        self.assertContains(response, tags["name"])
        self.assertContains(response, data["reviews"])
        self.assertContains(response, data["rating"])


class BannerListViewTsetCase(TestCase):
    """
    TestCase for BannerListView
    """
    @classmethod
    def setUpClass(cls):
        cls.category_one = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_one = Subcategory.objects.create(
            id=123001,
            category=cls.category_one,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.category_two = Category.objects.create(
            id=223,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_two = Subcategory.objects.create(
            id=223001,
            category=cls.category_two,
            title="computers",
            src="/4.png",
            alt="Image alt string"
        )
        cls.category_three = Category.objects.create(
            id=323,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_three = Subcategory.objects.create(
            id=323001,
            category=cls.category_three,
            title="mobile phones",
            src="/5.png",
            alt="Image alt string"
        )

        cls.product_tag = Tag.objects.create(
            name="Gaming",
        )
        cls.product_tag.category.set(
            [
                cls.subcategory_one,
                cls.subcategory_two,
                cls.subcategory_three
            ]
        )

        cls.product_one = Product.objects.create(
            category=cls.subcategory_one,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=True,
            available=True,
        )
        cls.product_one.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_one,
            src="/3.png",
            alt="Image alt string"
        )
        cls.user = User.objects.create_user("test", "test@test.test", "!@#$%67890qwerty")

        cls.product_review = Review.objects.create(
            product=cls.product_one,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_two = Product.objects.create(
            category=cls.subcategory_two,
            title="Asus Pro",
            description="",
            price=1600.67,
            count=5,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_two.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_two,
            src="/4.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_two,
            author=cls.user,
            rate=4,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_three = Product.objects.create(
            category=cls.subcategory_three,
            title="Google Pixel7",
            description="",
            price=800.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_three.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_three,
            src="/5.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_three,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )

    @classmethod
    def tearDownClass(cls):
        cls.product_review.delete()
        cls.product_image.delete()
        cls.product_one.delete()
        cls.product_two.delete()
        cls.product_three.delete()
        cls.subcategory_one.delete()
        cls.subcategory_two.delete()
        cls.subcategory_three.delete()
        cls.category_one.delete()
        cls.category_two.delete()
        cls.category_three.delete()
        cls.user.delete()

    def test_get(self):
        response = self.client.get(reverse("api:banners"))
        data = response.data[0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"])
        self.assertContains(response, data["category"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["count"])
        self.assertContains(response, data["date"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["description"])
        self.assertContains(response, str(data["freeDelivery"]).lower())
        self.assertContains(response, images["src"])
        self.assertContains(response, images["alt"])
        self.assertContains(response, tags["id"])
        self.assertContains(response, tags["name"])
        self.assertContains(response, data["reviews"])
        self.assertContains(response, data["rating"])


class BasketViewSetTestCase(TestCase):
    """
    TestCase for BasketViewSet
    """
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user("test_user", "test@test.test", "!@#$%67890qwerty")

        cls.category_one = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_one = Subcategory.objects.create(
            id=123001,
            category=cls.category_one,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.category_two = Category.objects.create(
            id=223,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_two = Subcategory.objects.create(
            id=223001,
            category=cls.category_two,
            title="computers",
            src="/4.png",
            alt="Image alt string"
        )
        cls.category_three = Category.objects.create(
            id=323,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_three = Subcategory.objects.create(
            id=323001,
            category=cls.category_three,
            title="mobile phones",
            src="/5.png",
            alt="Image alt string"
        )

        cls.product_tag = Tag.objects.create(
            name="Gaming",
        )
        cls.product_tag.category.set(
            [
                cls.subcategory_one,
                cls.subcategory_two,
                cls.subcategory_three
            ]
        )

        cls.product_one = Product.objects.create(
            category=cls.subcategory_one,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=True,
            available=True,
        )
        cls.product_one.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_one,
            src="/3.png",
            alt="Image alt string"
        )
        cls.user = User.objects.create_user("test_basket_user", "test@test.test", "!@#$%67890qwerty")

        cls.product_review = Review.objects.create(
            product=cls.product_one,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_two = Product.objects.create(
            category=cls.subcategory_two,
            title="Asus Pro",
            description="",
            price=1600.67,
            count=5,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_two.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_two,
            src="/4.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_two,
            author=cls.user,
            rate=4,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_three = Product.objects.create(
            category=cls.subcategory_three,
            title="Google Pixel7",
            description="",
            price=800.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_three.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_three,
            src="/5.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_three,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )

        cls.basket_one = Basket.objects.create(
            user=cls.user,
            date=datetime.date.today(),
            product=cls.product_one,
            count=5,
        )

        cls.basket_two = Basket.objects.create(
            user=cls.user,
            date=datetime.date.today(),
            product=cls.product_two,
            count=10,
        )

        cls.basket_three = Basket.objects.create(
            user=cls.user,
            date=datetime.date.today(),
            product=cls.product_three,
            count=2,
        )

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.basket_one.delete()
        cls.basket_two.delete()
        cls.basket_three.delete()
        cls.product_review.delete()
        cls.product_image.delete()
        cls.product_one.delete()
        cls.product_two.delete()
        cls.product_three.delete()
        cls.subcategory_one.delete()
        cls.subcategory_two.delete()
        cls.subcategory_three.delete()
        cls.category_one.delete()
        cls.category_two.delete()
        cls.category_three.delete()
        cls.user.delete()

    def test_get(self):
        response = self.client.get(reverse("api:basket-list"), content_type='application/json')
        data = response.data[0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"])
        self.assertContains(response, data["category"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["count"])
        self.assertContains(response, data["date"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["description"])
        self.assertContains(response, str(data["freeDelivery"]).lower())
        self.assertContains(response, images["src"])
        self.assertContains(response, images["alt"])
        self.assertContains(response, tags["id"])
        self.assertContains(response, tags["name"])
        self.assertContains(response, data["reviews"])
        self.assertContains(response, data["rating"])

    def test_post(self):
        post_data = {"id": self.product_three.id, "count": 5}
        response = self.client.post(reverse("api:basket-list"), data=post_data, content_type='application/json')
        data = response.data[0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"], status_code=201)
        self.assertContains(response, data["category"], status_code=201)
        self.assertContains(response, data["price"], status_code=201)
        self.assertContains(response, data["count"], status_code=201)
        self.assertContains(response, data["date"], status_code=201)
        self.assertContains(response, data["title"], status_code=201)
        self.assertContains(response, data["description"], status_code=201)
        self.assertContains(response, str(data["freeDelivery"]).lower(), status_code=201)
        self.assertContains(response, images["src"], status_code=201)
        self.assertContains(response, images["alt"], status_code=201)
        self.assertContains(response, tags["id"], status_code=201)
        self.assertContains(response, tags["name"], status_code=201)
        self.assertContains(response, data["reviews"], status_code=201)
        self.assertContains(response, data["rating"], status_code=201)

    def test_reduce_amount(self):
        post_data = {"id": self.product_three.id, "count": 1}
        response = self.client.delete(
            reverse("api:basket-list"),
            data=post_data,
            content_type='application/json',
        )
        data = response.data[0]
        images = data["images"][0]
        tags = data["tags"][0]
        self.assertContains(response, data["id"])
        self.assertContains(response, data["category"])
        self.assertContains(response, data["price"])
        self.assertContains(response, data["count"])
        self.assertContains(response, data["date"])
        self.assertContains(response, data["title"])
        self.assertContains(response, data["description"])
        self.assertContains(response, str(data["freeDelivery"]).lower())
        self.assertContains(response, images["src"])
        self.assertContains(response, images["alt"])
        self.assertContains(response, tags["id"])
        self.assertContains(response, tags["name"])
        self.assertContains(response, data["reviews"])
        self.assertContains(response, data["rating"])

    def test_delete(self):
        post_data = {"id": self.product_three.id, "count": 4}
        response = self.client.delete(
            reverse("api:basket-list"),
            data=post_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 204)


class OrderViewSetTestCase(TestCase):
    """
    TestCase for OrdersViewSet
    """
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user("test_oder_user", "test@test.test", "!@#$%67890qwerty")

        cls.category_one = Category.objects.create(
            id=123,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_one = Subcategory.objects.create(
            id=123001,
            category=cls.category_one,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.category_two = Category.objects.create(
            id=223,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_two = Subcategory.objects.create(
            id=223001,
            category=cls.category_two,
            title="computers",
            src="/4.png",
            alt="Image alt string"
        )
        cls.category_three = Category.objects.create(
            id=323,
            title="video card",
            src="/3.png",
            alt="Image alt string"
        )
        cls.subcategory_three = Subcategory.objects.create(
            id=323001,
            category=cls.category_three,
            title="mobile phones",
            src="/5.png",
            alt="Image alt string"
        )

        cls.product_tag = Tag.objects.create(
            name="Gaming",
        )
        cls.product_tag.category.set(
            [
                cls.subcategory_one,
                cls.subcategory_two,
                cls.subcategory_three
            ]
        )

        cls.product_one = Product.objects.create(
            category=cls.subcategory_one,
            title="video card",
            description="",
            price=500.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=True,
            available=True,
        )
        cls.product_one.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_one,
            src="/3.png",
            alt="Image alt string"
        )
        cls.user = User.objects.create_user("test", "test@test.test", "!@#$%67890qwerty")

        cls.product_review = Review.objects.create(
            product=cls.product_one,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_two = Product.objects.create(
            category=cls.subcategory_two,
            title="Asus Pro",
            description="",
            price=1600.67,
            count=5,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_two.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_two,
            src="/4.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_two,
            author=cls.user,
            rate=4,
            text="review text",
            date=datetime.date.today()
        )
        cls.product_three = Product.objects.create(
            category=cls.subcategory_three,
            title="Google Pixel7",
            description="",
            price=800.67,
            count=3,
            freeDelivery=True,
            date=datetime.date.today(),
            archived=False,
            limited=False,
            available=True,
        )
        cls.product_three.tags.set([cls.product_tag])

        cls.product_image = ProductImage.objects.create(
            product=cls.product_three,
            src="/5.png",
            alt="Image alt string"
        )

        cls.product_review = Review.objects.create(
            product=cls.product_three,
            author=cls.user,
            rate=5,
            text="review text",
            date=datetime.date.today()
        )

        cls.order_one = Order.objects.create(
            createdAt=datetime.date.today(),
            paymentType="online",
            deliveryType="ordinary",
            status="accepted",
            city="Moscow",
            address="Red Square, 1",
            fullName="Mikhail Nartsissov",
            email="mikhail@nartsissov.com",
            phone=79153333333,
            user=cls.user,
        )

        cls.order_two = Order.objects.create(
            createdAt=datetime.date.today(),
            paymentType="random",
            deliveryType="express",
            status="Awaiting payment",
            city="London",
            address="Trafalgar Square, 1",
            fullName="John Lennon",
            email="john@lennon.beatles",
            phone=104420333222,
            user=cls.user,
        )

        cls.order_three = Order.objects.create(
            createdAt=datetime.date.today(),
            paymentType="other",
            deliveryType="express",
            status="paid",
            city="Antananarivu",
            address="Patrice Lumumba street, 4843/455",
            fullName="Patrice Lumumba",
            email="patrice@lumumba.mad",
            phone=440420333222,
            user=cls.user,
        )
        cls.order_item_one = OrderItem.objects.create(
            order=cls.order_one,
            product=cls.product_one,
            count=2
        )
        cls.order_item_two = OrderItem.objects.create(
            order=cls.order_one,
            product=cls.product_two,
            count=2
        )
        cls.order_item_three = OrderItem.objects.create(
            order=cls.order_two,
            product=cls.product_three,
            count=2
        )

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.order_item_one.delete()
        cls.order_item_two.delete()
        cls.order_item_three.delete()
        cls.order_one.delete()
        cls.order_two.delete()
        cls.order_three.delete()
        cls.product_review.delete()
        cls.product_image.delete()
        cls.product_one.delete()
        cls.product_two.delete()
        cls.product_three.delete()
        cls.subcategory_one.delete()
        cls.subcategory_two.delete()
        cls.subcategory_three.delete()
        cls.category_one.delete()
        cls.category_two.delete()
        cls.category_three.delete()
        cls.user.delete()

    def test_get(self):
        response = self.client.get(reverse(
            "api:orders-list"),
            content_type='application/json',
        )
        for item in response.data:
            for product in item["products"]:
                # testing products data in the order
                images = product["images"]
                tags = product["tags"]
                for image in images:
                    self.assertContains(response, image["src"])
                    self.assertContains(response, image["alt"])
                for tag in tags:
                    self.assertContains(response, tag["id"])
                    self.assertContains(response, tag["name"])
                self.assertContains(response, product["reviews"])
                self.assertContains(response, product["rating"])
            # testing orders data in the orders list
            self.assertContains(response, item["id"])
            self.assertContains(response, item["createdAt"])
            self.assertContains(response, item["fullName"])
            self.assertContains(response, item["email"])
            self.assertContains(response, item["phone"])
            self.assertContains(response, item["deliveryType"])
            self.assertContains(response, item["paymentType"])
            self.assertContains(response, item["totalCost"])
            self.assertContains(response, item["status"])
            self.assertContains(response, item["city"])
            self.assertContains(response, item["address"])

    def test_post(self):
        request_data = [
            {
                "id": self.product_one.id,
                "category": self.product_one.category.id,
                "price": self.product_one.price,
                "count": 1,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": self.product_one.title,
                "description": self.product_one.description,
                "freeDelivery": "true",
                "images": [
                    {
                        "src": "/3.png",
                        "alt": "Image alt string"
                    }
                ],
                "tags": [
                    {
                        "id": self.product_tag.id,
                        "name": self.product_tag.name
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]

        response = self.client.post(reverse(
            "api:orders-list"),
            data=request_data,
            content_type='application/json',
        )
        self.assertContains(response, response.data["orderId"], status_code=201)

    def test_get_by_pk(self):
        response = self.client.get(reverse(
            "api:orders-detail",
            kwargs={
                    "pk": self.order_one.pk
                }
        ),
            content_type='application/json',
        )
        data = response.data
        for product in data["products"]:
            # testing products data in the order
            images = product["images"]
            tags = product["tags"]
            for image in images:
                self.assertContains(response, image["src"])
                self.assertContains(response, image["alt"])
            for tag in tags:
                self.assertContains(response, tag["id"])
                self.assertContains(response, tag["name"])
            self.assertContains(response, product["reviews"])
            self.assertContains(response, product["rating"])
        # testing order data
        self.assertContains(response, data["id"])
        self.assertContains(response, data["createdAt"])
        self.assertContains(response, data["fullName"])
        self.assertContains(response, data["email"])
        self.assertContains(response, data["phone"])
        self.assertContains(response, data["deliveryType"])
        self.assertContains(response, data["paymentType"])
        self.assertContains(response, data["totalCost"])
        self.assertContains(response, data["status"])
        self.assertContains(response, data["city"])
        self.assertContains(response, data["address"])

    def test_post_by_pk(self):
        request_data = {
                "orderId": self.order_one.id,
                "createdAt": "20/09/23 15:45:42",
                "fullName": "Hammil Peter",
                "phone": 104420222333,
                "email": "hammil@hammil.vdg",
                "deliveryType": "express",
                "city": "Enter city of the delivery",
                "address": "Enter address of the delivery",
                "paymentType": "someone",
                "status": "accepted",
                "totalCost": 0,
                "products": [
                    {
                        "id": self.product_one.id,
                        "category": self.product_one.category.id,
                        "price": self.product_one.price,
                        "count": 2,
                        "date": self.product_one.date,
                        "title": self.product_one.title,
                        "description": self.product_one.description,
                        "freeDelivery": "true",
                        "images": [
                            {
                                "src": "/products/product_10/images/Marantz_PM-10.png",
                                "alt": "There should be an image of the product"
                            }
                        ],
                        "tags": [
                            {
                                "id": self.product_tag.id,
                                "name": self.product_tag.name
                            }
                            ],
                        "reviews": 0,
                        "rating": "null"
                    }
                ],
                "paymentError": "null",
                "filters": {
                    "price":
                        {
                            "minValue": 1,
                            "maxValue": 500000,
                            "currentFromValue": 7,
                            "currentToValue": 27
                        }
                },
                "basket": {
                    self.product_one.id: {
                        "id": self.product_one.id,
                        "category": self.category_one.id,
                        "price": self.product_one.price,
                        "count": 2,
                        "date": "null",
                        "title": self.product_one.title,
                        "description": self.product_one.description,
                        "freeDelivery": "true",
                        "images": [
                            {
                                "src": "/products/product_10/images/Marantz_PM-10.png",
                                "alt": "There should be an image of the product"
                            }
                        ],
                        "tags": [
                            {
                                "id": self.product_tag.id,
                                "name": self.product_tag.name
                            }
                        ],
                        "reviews": 0,
                        "rating": "null"
                    }
                },
                "basketCount": {
                    "count": 2,
                    "price": 25999.98
                }
            }
        response = self.client.post(reverse(
            "api:orders-detail",
            kwargs={
                    "pk": self.order_one.id
                }
        ),
            data=request_data,
            content_type='application/json',
        )
        self.assertContains(response, response.data["orderId"])


class PaymentCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user("test_payment_user", "test@test.test", "!@#$%67890qwerty")

        cls.order_one = Order.objects.create(
            createdAt=datetime.date.today(),
            paymentType="online",
            deliveryType="ordinary",
            status="accepted",
            city="Moscow",
            address="Red Square, 1",
            fullName="Mikhail Nartsissov",
            email="mikhail@nartsissov.com",
            phone=79153333333,
            user=cls.user,
        )

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.order_one.delete()
        cls.user.delete()

    def test_post(self):
        request_data = {
            "number": "88888888",
            "name": "Annoying Orange",
            "month": "02",
            "year": "2025",
            "code": "123"
        }

        response = self.client.post(reverse(
            "api:payment_create", kwargs={"id": self.order_one.id}),
            data=request_data,
            content_type='application/json',
        )
        self.assertEquals(response.status_code, 201)
