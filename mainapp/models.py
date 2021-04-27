from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_item = self.order_item_set.all()
        for item in order_item:
            if not item.product.digital:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        order_item = self.order_item_set.all()
        total = sum([item.get_total for item in order_item])
        return total


    @property
    def get_cart_item(self):
        order_item = self.order_item_set.all()
        total = sum([item.quantity for item in order_item])
        return total


class Product(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    content = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='static/images/data_base/photos/')
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title

    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.ImageField(default=0, null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name


