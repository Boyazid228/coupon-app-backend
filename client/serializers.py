from rest_framework import serializers
from categories.models import *
from django.contrib.auth import get_user_model
from my_api.serializers import CouponSerializer, USelializer
from orders.models import Order
User = get_user_model()


class OrderSelializer(serializers.ModelSerializer):
    product = CouponSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(), source='product', write_only=True, required=False, allow_null=True
    )

    user = USelializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    owner = USelializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='owner', write_only=True
    )

    class Meta(object):
        model = Order
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    short_description = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    rating = serializers.FloatField(default=0)

    name_en = serializers.CharField(required=True)
    description_en = serializers.CharField(required=True)
    short_description_en = serializers.CharField(required=True)
    title_en = serializers.CharField(required=True)

    class Meta:
        model = Products

        fields = [
            'name', 'name_en', 'name_ko',
            'description', 'description_en', 'description_ko',
            'short_description', 'short_description_en', 'short_description_ko',
            'title', 'title_en', 'title_ko',

            'price', 'count',
            'background', 'preview',
            'shop', 'time_start', 'time_finish', 'rating'
        ]

    def create(self, validated_data):
        for base_field in ['name', 'description', 'short_description', 'title']:
            en_field = f"{base_field}_en"
            if en_field in validated_data:
                validated_data[base_field] = validated_data[en_field]

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        for base_field in ['name', 'description', 'short_description', 'title']:
            en_field = f"{base_field}_en"
            if en_field in validated_data:
                validated_data[base_field] = validated_data[en_field]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ShopUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    info = serializers.CharField(required=False)
    rating = serializers.FloatField(default=0)
    short_description = serializers.CharField(required=False)

    short_description_en = serializers.CharField(required=True)
    name_en = serializers.CharField(required=True)
    description_en = serializers.CharField(required=True)
    info_en = serializers.CharField(required=True)

    class Meta:
        model = Shops

        fields = [
            'name', 'name_en', 'name_ko',
            'description', 'description_en', 'description_ko',
            'short_description', 'short_description_en', 'short_description_ko',
            'info', 'info_en', 'info_ko',


            'background', 'preview', 'logo',
            'category',  'rating'
        ]

    def create(self, validated_data):
        for base_field in ['name', 'description', 'short_description', 'info']:
            en_field = f"{base_field}_en"
            if en_field in validated_data:
                validated_data[base_field] = validated_data[en_field]

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        for base_field in ['name', 'description', 'short_description', 'info']:
            en_field = f"{base_field}_en"
            if en_field in validated_data:
                validated_data[base_field] = validated_data[en_field]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ShopLocationsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopsLocations

        fields = [
            'latitude', 'longitude', 'address', 'shop', 'user'
        ]

    def create(self, validated_data):

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance