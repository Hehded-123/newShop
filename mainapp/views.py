from django.shortcuts import render, redirect
from .models import *
from .forms import ContactForm
from .guest_utils import cookieCart, cartData, guestOrder
import json
import datetime
from django.http import JsonResponse

def index(request):
    form = ContactForm()
    contact_us(request)
    categories = Category.objects.all()

    if request.method == "POST" and request.POST.get('category_id'):
        product_bd = Product.objects.filter(category=request.POST.get('category_id'))
    else:
        product_bd = Product.objects.all()

    data = {'form': form, 'product_bd': product_bd, 'categories': categories}
    return render(request, 'mainapp/index.html', data)


def brand(request):
    return render(request, "mainapp/brand.html")


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()

def proccessOrder(request):
    transaction_id = datetime.datetime.now() .timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.use.customer()
        order, created = OrderItem.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id =transaction_id

    if total == float(order.get_cart_total):
        order.complete=True
    order.save()

    if order.shipping==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            postal_code=data['shipping']['postal_code'],
        )


def contact(request):
    form = ContactForm()
    contact_us(request)
    data = {'form': form, }
    return render(request, 'mainapp/contact.html', data)


def specials(request):
    return render(request, 'mainapp/special.html')


def about(request):
    return render(request, 'mainapp/about.html')


def store(request, products=True):
    data = cartData(request)
    cartItem = data['cartItem']

    item = Product.objects.all()
    context = {
        'products': products,
        'cartItem': cartItem
    }

    return render(request, 'mainapp/index.html', context)


def checkout(request):
    data = cartData(request)
    cartItem = data['cartItem']
    order = data['orer']
    item = data['item']

    context = {'item': item, 'order': order, 'cartItem': cartItem}

    return render(request, context, 'mainapp/checkout.html')

def updateItem(request, order=None):
    data =json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('action': action)
    # print('productId': productId)


    customer = request.user.customer
    product = Product.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    if action == "add":
        orderItem.quantity = (orderItem.quantity+1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('Product was added', save=False)


