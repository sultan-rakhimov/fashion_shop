from django.shortcuts import render, reverse, redirect
from .models import Color, Category, Review, Size, Product
from .forms import UserForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404


def home(request):
    sizes = Size.objects.all()
    colors = Color.objects.all()
    products = Product.objects.all()
    return render(request, 'siteviewer/home.html', {'products': products, 'sizes': sizes, 'colors': colors})


def product_detail(request, slug):
    product = Product.objects.get(slug__iexact=slug)
    latest_reviews = product.reviews.order_by('-date')
    return render(request, 'siteviewer/product_detail.html', {'product': product, 'latest_reviews': latest_reviews})


def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'siteviewer/sign_up.html', {'form': form})


def reviews(request, slug):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(slug__iexact=slug)
            product.reviews.create(
                user=request.user,
                text=request.POST.get('review_text')
            )
            return redirect(reverse('product_detail_url', args=(slug,)))
        else:
            return redirect(reverse('product_detail_url', args=(slug,)))
    else:
        return redirect('home')


def filter(request):
    if request.method == 'POST':
        size = request.POST.get('size')  # id
        color = request.POST.get('color')  # id
        products = Product.objects.filter(
            Q(
                Q(sizes=size) and Q(colors=color)
            )
        )
    return render(request, 'siteviewer/home_filter.html', {'products': products})

    '''
        for color|size in colors|sizes:
        label>{{color.name}}|{{size.name}}
        input type=radio name=size|color value={{size.id}}|{{color.id}}
        '''
