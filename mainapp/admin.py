
from django.contrib import admin
from .models import Product, Contact, Category, Customer, Order, OrderItem, ShippingAddress

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)