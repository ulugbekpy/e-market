from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from uuid import uuid4
from .manager import UserManager
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self) -> str:
        return self.phone


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    icon = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Seller(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='seller')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    certificate = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)


class Shop(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(
        Category, related_name='product')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customers')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True,default=uuid4)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self) -> str:
        return self.product.title


class Order(models.Model):

    class StatusChoice(models.TextChoices):
        INCONFIRMED = 'I'
        PENDING = 'P'
        DELIVERED = 'D'
        CANCELLED = 'C'

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=1, choices=StatusChoice.choices, default=StatusChoice.INCONFIRMED)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')


class Favourite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)