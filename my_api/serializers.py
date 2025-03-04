from rest_framework import serializers
from categories.models import *
from django.contrib.auth import get_user_model

User = get_user_model()





class categorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    img = serializers.ImageField()
    link = serializers.CharField()


class shopsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    logo = serializers.ImageField()
    info = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
    rating = serializers.IntegerField()
    description = serializers.CharField()
    short_description = serializers.CharField()
    background = serializers.ImageField()
    preview = serializers.ImageField()


class shopSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    logo = serializers.ImageField()
    info = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
    rating = serializers.IntegerField()
    description = serializers.CharField()
    short_description = serializers.CharField()
    background = serializers.ImageField()
    preview = serializers.ImageField()
    review_count = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        count = Reviews.objects.filter(shop_id=obj.id).count()
        return count



class couponSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    rating = serializers.IntegerField()
    price = serializers.IntegerField()
    count = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    short_description = serializers.CharField()
    background = serializers.ImageField()
    preview = serializers.ImageField()
    shop = serializers.PrimaryKeyRelatedField(queryset=Shops.objects.all())
    review_count = serializers.SerializerMethodField()


    def get_review_count(self, obj):
        count = Reviews.objects.filter(product_id=obj.id).count()
        return count



# class couSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     rating = serializers.IntegerField()
#     price = serializers.IntegerField()
#     count = serializers.IntegerField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     short_description = serializers.CharField()
#     background = serializers.ImageField()
#     preview = serializers.ImageField()
#     shop = serializers.PrimaryKeyRelatedField(queryset=Shops.objects.all())


class UserSelializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class USelializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username',  'email']


class marksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    shop = shopsSerializer()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ReviewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = couponSerializer()
    user = USelializer()
    shop = shopsSerializer()
    grade = serializers.IntegerField()
    date = serializers.DateTimeField(required=False)
    description = serializers.CharField(style={'base_template': 'textarea.html'})


class VlogsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = USelializer()
    likes = serializers.IntegerField()
    img = serializers.ImageField()
    description = serializers.CharField()
    date = serializers.DateTimeField(required=False)


class LikesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Optional customization
    shop = serializers.PrimaryKeyRelatedField(queryset=Shops.objects.all())  # Assuming a Shop model

    class Meta:
        model = Favorites
        fields = ['id', 'user', 'shop']



class LikesGetSerializer(serializers.ModelSerializer):
    user = USelializer()
    shop = shopSerializer()

    class Meta:
        model = Favorites
        fields = ['id', 'user', 'shop']
