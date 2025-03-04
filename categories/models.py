from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings


# Create your models here.
def categories_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "categories_{0}/{1}".format(instance.name, filename)


def shops_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "shops_{0}/{1}".format(instance.name, filename)


def vlogs_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "vlogs_{0}/{1}".format(instance.user.username, filename)

class Categories(models.Model):
    name = models.CharField(max_length=255, null=True)
    img = models.ImageField(upload_to=categories_directory_path, max_length=200)
    link = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Shops(models.Model):
    name = models.CharField(blank=True, max_length=255)
    logo = models.ImageField(upload_to=shops_directory_path, max_length=200)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True)
    description = RichTextField()
    short_description = models.TextField()
    info = RichTextField()
    background = models.ImageField(upload_to=shops_directory_path, max_length=200, default="")
    preview = models.ImageField(upload_to=shops_directory_path, max_length=200, default="")

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return self.name


class ShopsLocations(models.Model):
    shop = models.ForeignKey('Shops',  on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name = 'Shop Location'
        verbose_name_plural = 'Shop Locations'

    def __str__(self):
        return self.shop.name


class Products(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.IntegerField()
    title = models.CharField(max_length=255)
    description = RichTextField()
    short_description = RichTextField( default="")
    background = models.ImageField(upload_to=shops_directory_path, max_length=200, default="")
    preview = models.ImageField(upload_to=shops_directory_path, max_length=200, default="")
    shop = models.ForeignKey('Shops', on_delete=models.CASCADE, default="")
    time_start = models.DateTimeField(null=True, editable=True)
    time_finish = models.DateTimeField(null=True, editable=True)


    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shops', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, blank=True, null=True)
    grade = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    description = RichTextField()

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shops', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'


class Vlogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=vlogs_directory_path, max_length=200, default="")
    description = RichTextField()
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vlog'
        verbose_name_plural = 'Vlogs'


