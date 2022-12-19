from django.core.validators import EmailValidator

from django.utils import timezone
from django.db import models

'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    fio = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=150, blank=True)
    device = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'''


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Имя клиента')
    email = models.CharField(max_length=12, null=True, blank=True, validators=[EmailValidator], verbose_name='Почта')
    device = models.CharField(max_length=200, null=True, blank=True, verbose_name='ID устройства')

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название фирмы')
    origin = models.CharField(max_length=50, null=True, verbose_name='Страна изготовления')
    tel = models.CharField(max_length=14, blank=False, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фирма'
        verbose_name_plural = 'Фирмы'


class Category(models.Model):
    image = models.ImageField(upload_to='item_pictures/', default='default.png', null=False, verbose_name='Изображение')
    name = models.CharField(max_length=20, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    email = models.CharField(max_length=50, verbose_name='Email')
    phone = models.CharField(max_length=50, blank=False, verbose_name='Телефон')
    address = models.CharField(max_length=50, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Batch(models.Model):
    date = models.DateField(verbose_name='Дата')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='Поставщик')

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    def __str__(self):
        return f'{self.provider} - {self.date}'


class Item(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    description = models.CharField(max_length=200, blank=False, verbose_name='Описание')
    image = models.ImageField(upload_to='item_pictures/', null=False, verbose_name='Изображение', default='default.png')
    price = models.FloatField(null=False, verbose_name='Цена')
    count = models.IntegerField(verbose_name='Количество')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставка')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Фирма')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')

    class Condition(models.TextChoices):
        NEW = 'NEW', 'Новый'
        USED = 'USED', 'Б/у'
        DISCOUNT = 'DISCOUNT', 'Уценка'

    condition = models.CharField(
        max_length=10,
        choices=Condition.choices,
        default=Condition.NEW,
        blank=False,
        verbose_name='Состояние'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    order_date = models.DateField(null=False, default=timezone.now, verbose_name='Дата размещения заказа')
    completion_date = models.DateField(null=True, blank=True, default=None, verbose_name='Дата выполнения заказа')
    completed = models.BooleanField(null=True, blank=True, default=False, verbose_name='Выполнен')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, verbose_name='Клиент')
    token = models.CharField(null=True, max_length=10)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        ordereditems = self.ordereditem_set.all()
        total = sum([item.get_total for item in ordereditems])
        return total

    @property
    def get_cart_items(self):
        ordereditems = self.ordereditem_set.all()
        total = sum([item.quantity for item in ordereditems])
        return total


class OrderedItem(models.Model):
    count = models.PositiveIntegerField(null=False, default=1, verbose_name='Количество')
    cost = models.FloatField(null=True, verbose_name='Цена')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        verbose_name = 'Заказ товаров'
        verbose_name_plural = 'Заказы товаров'

    def __str__(self):
        return str(self.pk)

    @property
    def get_total(self):
        total = self.item.price * self.count
        self.cost = total
        return total


class PickupAddress(models.Model):
    details = models.CharField(max_length=200, blank=False, verbose_name='Содержание')

    class Meta:
        verbose_name = 'Адрес самовывоза'
        verbose_name_plural = 'Адрес самовывоза'

    def __str__(self):
        return self.details
