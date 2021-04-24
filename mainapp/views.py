from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ContactForm


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


def contact(request):
    form = ContactForm()
    contact_us(request)
    data = {'form': form, }
    return render(request, 'mainapp/contact.html', data)


def specials(request):
    return render(request, 'mainapp/special.html')


def about(request):
    return render(request, 'mainapp/about.html')
