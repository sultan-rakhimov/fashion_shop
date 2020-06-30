from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify


colors = (('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'),
          ('black', 'Black'), ('white', 'White'))


class Color(models.Model):
    title = models.CharField('Title', choices=colors, max_length=128)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def get_absolute_url(self):
        return reverse('color_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


sizes = (('S', 'Small'), ('M', 'Medium'), ('L', 'Large'),
         ('XL', 'Extra Large'), ('XXL', 'Double Extra Large'))


class Size(models.Model):
    title = models.CharField('Title', choices=sizes, max_length=128)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def get_absolute_url(self):
        return reverse('size_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


categories = (('W', 'Winter'), ('Sp', 'Spring'), ('Sm', 'Summer'), ('F', 'Fall'),
              ('W-F', 'Winter-Fall'), ('Sp-Sm', 'Spring-Summer'))


class Category(models.Model):
    title = models.CharField('Title', choices=categories, max_length=128)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField('Title', max_length=128)
    image = models.ImageField('Image')


class Product(models.Model):
    user = models.ForeignKey(
        'auth.User', related_name='products', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description', max_length=1000)
    image = models.ImageField('Poop-up Image')
    slug = models.SlugField('URL', unique=True)
    categories = models.ManyToManyField(Category, related_name="products")
    colors = models.ManyToManyField(Color, related_name="products")
    sizes = models.ManyToManyField(Size, related_name="products")
    images = models.ManyToManyField(Image, null=True, blank=True)
    date = models.DateTimeField(
        'Date', default=timezone.now)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        slug = self.slug
        return reverse('product_detail_url', kwargs={'slug': slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    user = models.ForeignKey(
        'auth.User', related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField('Text', max_length=500)
    status = models.BooleanField('Status', default=False)
    date = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    rate = models.IntegerField('Rating', default=0)
