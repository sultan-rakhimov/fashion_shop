from django.shortcuts import render, reverse, redirect
from .models import Color, Category, Review, Size, Product
from .forms import UserForm, CreateProduct, UpdateProduct
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from .serializers import ProductSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def api_products_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
