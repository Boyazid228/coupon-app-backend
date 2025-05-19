from rest_framework import serializers
from categories.models import *
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = ['id', 'name', 'img', 'link']

    def get_name(self, obj):
        lang = self.context.get('lang', 'en')
        name_field = f'name_{lang}'
        return getattr(obj, name_field, obj.name) or obj.name


class BaseShopSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all())
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Shops
        fields = ['id', 'name', 'logo', 'info', 'category', 'rating',
                  'description', 'short_description', 'background', 'preview']

    def get_localized_field(self, obj, field_base_name):
        lang = self.context.get('lang', 'en')
        localized_field = f'{field_base_name}_{lang}'
        default = getattr(obj, field_base_name, '')
        return getattr(obj, localized_field, default) or default

    def get_name(self, obj):
        return self.get_localized_field(obj, 'name')

    def get_info(self, obj):
        return self.get_localized_field(obj, 'info')

    def get_description(self, obj):
        return self.get_localized_field(obj, 'description')

    def get_short_description(self, obj):
        return self.get_localized_field(obj, 'short_description')


class ShopsSerializer(BaseShopSerializer):
    pass


class ShopSerializer(BaseShopSerializer):
    review_count = serializers.SerializerMethodField()

    class Meta(BaseShopSerializer.Meta):
        fields = BaseShopSerializer.Meta.fields + ['review_count']

    def get_review_count(self, obj):
        return Reviews.objects.filter(shop_id=obj.id).count()


class CouponSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    shop = serializers.PrimaryKeyRelatedField(queryset=Shops.objects.all())
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'count', 'shop', 'rating', 'description', 'short_description', 'background',
                  'preview', 'review_count', 'title', 'info', 'time_start', 'time_finish']

    def get_localized_field(self, obj, field_base_name):
        lang = self.context.get('lang', 'en')
        localized_field = f'{field_base_name}_{lang}'
        default = getattr(obj, field_base_name, '')
        return getattr(obj, localized_field, default) or default

    def get_name(self, obj):
        return self.get_localized_field(obj, 'name')

    def get_info(self, obj):
        return self.get_localized_field(obj, 'info')

    def get_description(self, obj):
        return self.get_localized_field(obj, 'description')

    def get_short_description(self, obj):
        return self.get_localized_field(obj, 'short_description')

    def get_review_count(self, obj):
        return Reviews.objects.filter(product_id=obj.id).count()


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
    shop = ShopsSerializer()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ReviewsSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    product = CouponSerializer()

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ['id', 'date']


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
    shop = ShopSerializer()

    class Meta:
        model = Favorites
        fields = ['id', 'user', 'shop']


class OrderSelializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Optional customization
    product = CouponSerializer()  # Assuming a Shop model

    class Meta(object):
        model = Order
        fields = ['id', 'user', 'product', 'status', 'payment']