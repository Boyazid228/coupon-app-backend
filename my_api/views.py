# my_api/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from categories.models import *
from .serializers import (
    ReviewsSerializer,
    UserSelializer,
    categorySerializer,
    LikesGetSerializer,
    couponSerializer,
    marksSerializer,
    shopSerializer,
    shopsSerializer,
    VlogsSerializer,
    LikesSerializer
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
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
        serializer = ReviewsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def menu_list(request):
    if request.method == 'GET':
        menu = Categories.objects.all()
        serializer = categorySerializer(menu, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def getShops(request, id):
    if request.method == 'GET':

        category = Categories.objects.get(pk=id)
        shops = Shops.objects.filter(category__id=category.id)
        serializer = shopsSerializer(shops, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def getShop(request, id):
    if request.method == 'GET':
        shop = Shops.objects.get(pk=id)
        serializer = shopSerializer(shop)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getCoupons(request, id):
    if request.method == 'GET':
        coupons = Products.objects.filter(shop__id=id)
        serializer = couponSerializer(coupons, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def getMarks(request):
    if request.method == 'GET':
        marks = ShopsLocations.objects.all()
        serializer = marksSerializer(marks, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getCoupon(request, id):
    if request.method == 'GET':
        coupon = Products.objects.get(pk=id)
        serializer = couponSerializer(coupon)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getHots(request):
    if request.method == 'GET':
        coupons = Products.objects.order_by("rating")[:10:-1]
        serializer = couponSerializer(coupons, many=True)
        return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def signup(request):
    serializer = UserSelializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
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
        print(request)
        user = request.user
        user_data = {
            'username': user.username,
            'email': user.email,
            'id': user.id
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
        serializer = LikesSerializer(likes, many=True)
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
        serializer = LikesGetSerializer(likes, many=True)
        return JsonResponse(serializer.data, safe=False)






