from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail_url'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('products/<slug:slug>/reviews/', views.reviews, name='reviews'),
    path('products_filter/', views.filter, name='filter')
]
