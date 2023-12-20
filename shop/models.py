from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image

import time

img_width = 1000
img_height = 850


def gen_slug(str_to_slug):
    new_sl = slugify(str_to_slug, allow_unicode=True)
    return new_sl + '-' + str(int(time.time()))


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"<Category name: {self.name}>"


class Product(models.Model):
    # id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True, default='null')
    name = models.CharField(max_length=128, verbose_name='Model')
    description = models.TextField(blank=True, verbose_name='Description')
    image = models.ImageField(verbose_name='Image')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    producer = models.CharField(max_length=64, verbose_name='Producer')
    producerCountry = models.CharField(max_length=64, verbose_name='Producer country')

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    # creation_date = models.DateTimeField()

    def __str__(self):
        return f"<Product id: {self.id} name: {self.name}>"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name[:25])
        super().save(*args, **kwargs)

        print(self.image.path)

        img = Image.open(self.image.path)
        if img.width != img_width or img.height != img_height:
            resized_img = img.resize((img_width, img_height))
            resized_img.save(self.image.path, quality=90)
        # super().save(*args, **kwargs)


class Order(models.Model):

    user = models.ForeignKey(User, verbose_name='User', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name='Product', null=True , on_delete=models.SET_NULL)

    deliveryAddress = models.CharField(max_length=128, verbose_name='Delivery address')
    # payment = models.CharField(max_length=255, verbose_name='Payment')
    order_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"<Order id: {self.id} product: {self.product} user: {self.user}>"


class Feedback(models.Model):

    user = models.ForeignKey(User, verbose_name='User', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name='Product', null=True, on_delete=models.CASCADE)

    feedback_text = models.TextField(blank=True, max_length=512, verbose_name='Description')
    feedback_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"<Feedback id: {self.id} product: {self.product.id} user: {self.user}>"
