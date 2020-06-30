from django.contrib import admin
from .models import Product, Category, Color, Size, Review, Image


class SlugAdmin(admin.ModelAdmin):
    prepolated_fields = {'slug': ('title',)}


admin.site.register(Product, SlugAdmin)
admin.site.register(Category, SlugAdmin)
admin.site.register(Color, SlugAdmin)
admin.site.register(Size, SlugAdmin)
admin.site.register(Image, SlugAdmin)
admin.site.register(Review)
