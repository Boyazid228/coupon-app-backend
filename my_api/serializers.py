from rest_framework import serializers
from categories.models import *
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()


class UserSelializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class USelializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta(object):
        model = User
        fields = ['id', 'username',  'email',  'groups']


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
    category = CategorySerializer()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    user = USelializer()

    class Meta:
        model = Shops
        fields = ['id', 'name', 'logo', 'info', 'category', 'rating',
                  'description', 'short_description', 'background', 'preview', 'user']

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
    shop = ShopSerializer()
    user = USelializer()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'count', 'shop', 'rating', 'description', 'short_description', 'background',
                  'preview', 'review_count', 'title', 'info', 'time_start', 'time_finish', 'user']

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



class marksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    shop = ShopsSerializer()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    user = USelializer()
    address = serializers.CharField()


class ReviewsSerializer(serializers.ModelSerializer):
    user = USelializer(read_only=True)  # read_only
    owner = USelializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='owner', write_only=True)
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Shops.objects.all(), source='shop', write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), source='product', write_only=True,
                                                    required=False, allow_null=True)
    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ['id', 'date', 'user', 'owner']


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


