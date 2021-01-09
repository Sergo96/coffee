from django.db import models


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Customer(models.Model):
    GENDER = (
        ("male", "male"),
        ("female", "female"),
    )

    username = models.CharField(max_length=70, blank=True, null=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=70)
    date_birth = models.DateField(max_length=40)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER)

    def __str__(self):
        return self.username


class Trade(models.Model):
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True)
    price = models.FloatField()
    discount_id = models.ManyToManyField('Discount', blank=True)
    user_id = models.ForeignKey('Customer', blank=True, null=True, on_delete=models.CASCADE)
    location = models.TextField(max_length=100)
    packaging = models.ForeignKey('Package', blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class Product(models.Model):
    name = models.CharField(max_length=150)
    info = models.TextField(max_length=300)
    store_product = models.ForeignKey('Store', blank=True, null=True, on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', blank=True)
    stock = models.BooleanField()
    exp_date = models.DateTimeField()
    product_size = models.PositiveSmallIntegerField()
    product_weight = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{},{}'.format(self.name, self.info)


class Ratings(models.Model):
    product_id = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE)
    product_rating = IntegerRangeField(blank=True, max_value=5, min_value=0)
    store_rating = IntegerRangeField(blank=True, max_value=5, min_value=0)
    delivery_rating = IntegerRangeField(blank=True, max_value=5, min_value=0)
    package_rating = IntegerRangeField(blank=True, max_value=5, min_value=0)

    def __str__(self):
        return '{} {}'.format(self.product_rating, self.store_rating)


class Category(models.Model):
    category = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return '{}'.format(self.category)


class Store(models.Model):
    store_name = models.CharField(max_length=80)
    store_phone = models.CharField(max_length=13)
    store_address = models.CharField(max_length=150)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.store_name)


class Discount(models.Model):
    products_id = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', blank=True, null=True, on_delete=models.CASCADE)
    discount_start_time = models.DateTimeField(blank=True, null=True)
    discount_end_time = models.DateTimeField(blank=True, null=True)
    discount_type = models.CharField(max_length=200)
    discount_review = models.TextField(max_length=1000)

    def __str__(self):
        return '{}''{}'.format(self.products_id, self.store_id)


class UserAction(models.Model):
    user_id = models.ForeignKey('Customer', blank=True, null=True, on_delete=models.CASCADE)
    action_type = models.ForeignKey('ActionType', blank=True, null=True, on_delete=models.CASCADE)
    action_rang = models.ForeignKey('ActionRangType', blank=True, null=True, on_delete=models.CASCADE)
    during = models.DateTimeField(auto_now=False, auto_now_add=False)
    ended = models.BooleanField()

    def __str__(self):
        return '{} '.format(self.id)


class ActionType(models.Model):
    type = models.CharField(max_length=150)
    rang = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} '.format(self.type)


class ActionRangType(models.Model):
    rang_name = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} '.format(self.rang_name)


class Delivery(models.Model):
    user_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product_id = models.ManyToManyField('Product', blank=True)
    package_id = models.ManyToManyField('Package', blank=True)
    trade_id = models.ForeignKey('Trade', blank=True, null=True, on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', blank=True, null=True, on_delete=models.CASCADE)
    delivery_type = models.ForeignKey('DeliveryType', blank=True, null=True, max_length=150, on_delete=models.CASCADE)
    delivery_price = models.PositiveSmallIntegerField(blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    during = models.DateTimeField(auto_now=False, auto_now_add=False)
    delivery_status = models.ForeignKey('Ratings', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.id, self.delivery_price)


class DeliveryType(models.Model):
    type = models.CharField(max_length=150)


class Package(models.Model):
    package_type = models.CharField(max_length=70)
    package_price = models.IntegerField(blank=True)
    package_desc = models.TextField(max_length=100)
    package_volumn = models.IntegerField(blank=True)
    package_avarage_weight = models.TextField(max_length=300)
    image = models.ImageField(blank=True)
    package_images = models.ImageField(blank=True)

    def __str__(self):
        return '{}'.format(self.package_type)


class Review(models.Model):
    comments = models.TextField(max_length=400)
    store_id = models.ForeignKey('Store', blank=True, null=True, on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE)
