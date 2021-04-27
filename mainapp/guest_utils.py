import json
from .models import Product, Contact, Category, Customer, Order, OrderItem, ShippingAddress


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart: ', cart)
    item = []
    order = {'get_cart_total':0, 'get_cart_item':0, 'shipping': False }
    cartItem = order['get_cart_item']


    for i in cart:
        try:
            cartItem += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_item'] += cart[i]['quantity']

            item = {
                'product' : {'id': product.id, 'name': product.name,
                'price': product.price, 'imageURL': product.imageURL},
                'quantity': cart[i]['quantity'], 'get_total': total,
            }
            item.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass
    return {'cartItem': cartItem, 'order': order, 'item': item}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.order_item_set.all()
        cartItem = order.get_cart_item

    else:
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']
        order = cookieData['order']
        item = cookieData['item']

    return {'cartItem': cartItem, 'order': order, 'item': item}

def guestOrder(request,data):
    name = data['form']['name']
    email = data['form']['data']

    cookieData = cookieCart(request)
    item = cookieData['item']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in item:
        product =Product.objects.get(id=item['product']['id'])
        orderItem =OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

        return customer, order