from django.shortcuts import render, reverse, redirect
from .models import Color, Category, Review, Size, Product
from .forms import UserForm, CreateProduct, UpdateProduct
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView


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


def create_product(request):
    if request.method == 'POST':
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(user=request.user)
            product.colors.add(request.POST.get('colors'))
            product.sizes.add(request.POST.get('sizes'))
            product.categories.add(request.POST.get('categories'))
            product.save()
            return redirect(reverse('product_detail_url', args=(product.slug,)))
    else:
        form = CreateProduct()
    return render(request, 'siteviewer/product_form.html', {'form': form})


def delete_product(request, id):
    product = Product.objects.get(id=id)
    if product.user == request.user:
        if request.method == 'POST':
            product.delete()
    return redirect('home')


def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UpdateProduct(instance=product)
    return render(request, 'siteviewer/product_edit.html', {'form': form, 'product': product})
