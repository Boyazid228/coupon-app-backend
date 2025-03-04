from django.contrib import admin
from .models import *
from django.utils.html import format_html



@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 100px; " />'.format(obj.img.url))

    image_tag.short_description = 'Image'

    list_display = ['name', 'image_tag']


class ShopsLocationsInline(admin.TabularInline):
    model = ShopsLocations
    extra = 1


@admin.register(Shops)
class ShopsAdmin(admin.ModelAdmin):
    inlines = [ShopsLocationsInline]
    list_display = ['name', 'image_tag', 'rating']
    list_filter = ('name', 'rating')
    search_fields = ('name',)

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 100px; " />'.format(obj.logo.url))

    image_tag.short_description = 'Image'


@admin.register(ShopsLocations)
class ShopsLocationsAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'image_tag', 'latitude', 'longitude')
    list_filter = ('shop__name',)
    search_fields = ('shop__name',)


    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 100px; " />'.format(obj.shop.logo.url))

    image_tag.short_description = 'Image'

    def shop_name(self, instance):
        return instance.shop.name

    shop_name.short_description = 'Shop Name'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'shop_name', 'rating')
    list_filter = ('name', 'price', 'count', 'shop__name', 'rating', 'time_start', 'time_finish')
    search_fields = ('name', 'price', 'shop__name')

    def shop_name(self, instance):
        return instance.shop.name


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'product_name', 'shop_name', 'grade', 'date')
    list_filter = ('date', 'grade', 'user__username', 'product__name', 'shop__name',)
    search_fields = ('user__username', 'product__name', 'shop__name')

    def shop_name(self, instance):
        return instance.shop.name

    def user_name(self, instance):
        return instance.user.username

    def product_name(self, instance):
        return instance.product.name if instance.product else "-------"


@admin.register(Vlogs)
class VlogsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'image_tag', 'date', 'likes')

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 100px; " />'.format(obj.img.url))

    def user_name(self, instance):
        return instance.user.username




