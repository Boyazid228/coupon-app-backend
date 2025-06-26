
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from categories.models import *
from client.serializers import OrderSelializer
from .serializers import (
    ReviewsSerializer,
    UserSelializer,
    CategorySerializer,
    LikesGetSerializer,
    CouponSerializer,
    marksSerializer,
    ShopSerializer,
    ShopsSerializer,
    VlogsSerializer,
    LikesSerializer,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from orders.models import Order, Products
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group

import requests
import json


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_list(request, id, type):
    if request.method == 'GET':
        if type == "shop":
            reviews = Reviews.objects.filter(shop_id=id)
        else:
            reviews = Reviews.objects.filter(product_id=id)
        serializer = ReviewsSerializer(reviews, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':

        data = JSONParser().parse(request)

        if not request.user or request.user.is_anonymous:
            return JsonResponse({"error": "Authentication required."}, status=401)

        data['shop_id'] = data.get('shop')

        if type == "coupon":

            try:

                product = Products.objects.get(id=id)

            except Products.DoesNotExist:

                return JsonResponse({"error": "Product not found."}, status=404)

            data['shop_id'] = product.shop.id

            data['product_id'] = id

        else:

            data['shop_id'] = data.get('shop')

            data['product_id'] = None

        data['user_id'] = int(request.user.id)
        print(data)
        prod = Shops.objects.get(id=data.get('shop_id'))
        data['owner_id'] = prod.user.id
        data.pop('owner', None)
        data.pop('user', None)
        data.pop('shop', None)
        data.pop('product', None)
        print(data)
        serializer = ReviewsSerializer(data=data, context={'request': request})

        if serializer.is_valid():

            review = serializer.save()

            shop_id = review.shop.id if review.shop else None

            if shop_id:
                avg_grade_shop = Reviews.objects.filter(shop_id=shop_id).aggregate(Avg('grade'))['grade__avg']

                shop = Shops.objects.get(id=shop_id)

                shop.rating = round(avg_grade_shop or 0, 1)

                shop.save()



            if type == "coupon" and review.product:
                product_id = review.product.id

                avg_grade = Reviews.objects.filter(product_id=product_id).aggregate(Avg('grade'))['grade__avg']

                product = Products.objects.get(id=product_id)

                product.rating = round(avg_grade or 0, 1)

                product.save()



            return JsonResponse(serializer.data, status=201)
        print("Serializer errors:", serializer.errors)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def menu_list(request):
    if request.method == 'GET':
        lang = request.headers.get('Accept-Language', 'en')[:2]
        menu = Categories.objects.all()
        serializer = CategorySerializer(menu, many=True, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_shops(request, id):
    if request.method == 'GET':
        category = Categories.objects.get(pk=id)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        shops = Shops.objects.filter(category__id=category.id)
        serializer = ShopsSerializer(shops, many=True, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_shop(request, id):
    if request.method == 'GET':
        shop = Shops.objects.get(pk=id)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = ShopSerializer(shop, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_coupons(request, id):
    if request.method == 'GET':
        coupons = Products.objects.filter(shop__id=id)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = CouponSerializer(coupons, many=True, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def getMarks(request):
    if request.method == 'GET':
        marks = ShopsLocations.objects.all()
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = marksSerializer(marks, many=True, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getCoupon(request, id):
    if request.method == 'GET':
        coupon = Products.objects.get(pk=id)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = CouponSerializer(coupon, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getHots(request):
    if request.method == 'GET':
        coupons = Products.objects.order_by("rating")[:10:-1]
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = CouponSerializer(coupons, many=True, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def signup(request):
    serializer = UserSelializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        try:
            group = Group.objects.get(name='user')
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.groups.add(group)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data,
        }, status=status.HTTP_201_CREATED)

        # Return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        groups = user.groups.all()
        group_names = [group.name for group in groups]
        user_data = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'groups': group_names
        }
        return JsonResponse(user_data, safe=False)


class VlogsView(APIView):

    def get(self, request):
        vlogs = Vlogs.objects.all()
        serializer = VlogsSerializer(vlogs, many=True)
        return JsonResponse(serializer.data, safe=False)


class LikesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter likes by the authenticated user
        likes = Favorites.objects.filter(user=request.user)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = LikesSerializer(likes, many=True,  context={'lang': lang})
        return Response(serializer.data)  # Use DRF Response

    def post(self, request):
        # Automatically associate the like with the authenticated user
        data = request.data.copy()
        user = request.user
        shop_id = request.data.get('shop')

        # Check if a favorite already exists for this user and shop
        if Favorites.objects.filter(user_id=user, shop_id=shop_id).exists():
            return Response(
                {'status': 'error', 'message': 'You have already liked this shop.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LikesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetLikesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Filter likes by the authenticated user
        likes = Favorites.objects.filter(user=request.user)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = LikesGetSerializer(likes, many=True, context={'lang': lang})
        return JsonResponse(serializer.data, safe=False)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        lang = request.headers.get('Accept-Language', 'en')[:2]
        serializer = OrderSelializer(orders, many=True, context={'lang': lang})
        return Response(serializer.data)  # Use DRF Response

    def post(self, request):
        data = request.data.copy()
        prod = Products.objects.get(id=data['product'])
        data['product_id'] = int(data['product'])
        data['product'] = prod
        data['user_id'] = request.user.id
        data['user'] = request.user
        data['owner'] = User.objects.get(id=prod.user.id)
        data['owner_id'] = prod.user.id
        print(data)
        serializer = OrderSelializer(data=data)

        if serializer.is_valid():
            order = serializer.save()
            return Response({'status': "ok"}, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Reviews.objects.filter(user=request.user)
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data)  # Use DRF Response


