from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail_url'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('products/<slug:slug>/reviews/', views.reviews, name='reviews'),
    path('product/new/', views.create_product, name='product_create'),
    path('products_filter/', views.filter, name='filter'),
    path('product/<int:id>/edit/',
         views.update_product, name="edit_product"),
    path('product/<int:id>/delete/',
         views.delete_product, name="delete_product")
]
