from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse

from categories.models import *
from itertools import chain
from rest_framework import status
from datetime import datetime
from client.serializers import ProductUpdateSerializer, ShopUpdateSerializer, ShopLocationsUpdateSerializer, \
    OrderSelializer
from my_api.serializers import CouponSerializer, ShopSerializer, ReviewsSerializer, marksSerializer
from orders.models import Order, Products
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
import json
from collections import defaultdict
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.views import View
from django.db.models import Value, CharField
from django.core.exceptions import ObjectDoesNotExist
from dateutil import parser


class ClientProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Products.objects.filter(user=request.user)
        serializer = CouponSerializer(products, many=True)
        return Response(serializer.data)


model_map = {
    'product': Products,
    'shop': Shops,
    'review': Reviews,
    'location': ShopsLocations
}


class ClientItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, type, id):

        model = model_map.get(type)
        if not model:
            return Response({"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = model.objects.get(id=id, user=request.user)
        except ObjectDoesNotExist:
            return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        data = model_to_dict(instance)

        if type == 'product':
            data['shop'] = instance.shop.id if instance.shop else None
            data['background'] = instance.background.url if instance.background else None
            data['preview'] = instance.preview.url if instance.preview else None
        elif type == 'shop':
            data['background'] = instance.background.url if instance.background else None
            data['preview'] = instance.preview.url if instance.preview else None
            data['logo'] = instance.logo.url if instance.logo else None
            data['category'] = instance.category.id if instance.category else None
        elif type == 'location':
            data['shop'] = instance.shop.id if instance.shop else None

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, type, id):
        model = model_map.get(type)
        if not model:
            return Response({"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = model.objects.get(id=id, user=request.user)
        except ObjectDoesNotExist:
            return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        if type == 'product':
            serializer = ProductUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif type == 'shop':
            serializer = ShopUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif type == 'location':
            serializer = ShopLocationsUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Update not supported for this type"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, type, id=None):
        model = model_map.get(type)
        if not model:
            return Response({"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        if type == 'product':
            data = request.data.copy()
            data['user'] = request.user.id

            serializer = ProductUpdateSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'created'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif type == 'location':
            data = request.data.copy()
            data['user'] = request.user.id

            serializer = ShopLocationsUpdateSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'created'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif type == 'shop':
            data = request.data.copy()
            data['user'] = request.user.id

            serializer = ShopUpdateSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'created'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Creation not supported for this type"}, status=status.HTTP_400_BAD_REQUEST)


class ClientShops(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shops = Shops.objects.filter(user=request.user)
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)


class ClientReviews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get('id')
        type_ = request.GET.get('type')
        if type_ == 'product':
            reviews = Reviews.objects.filter(owner=request.user, product_id=id)
        elif type_ == 'shop':
            reviews = Reviews.objects.filter(owner=request.user, shop_id=id)
        else:
            return Response({"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data)


class ClientLocations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shops = ShopsLocations.objects.filter(user=request.user)
        serializer = marksSerializer(shops, many=True)
        return Response(serializer.data)


class ClientOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(owner=request.user)
        serializer = OrderSelializer(orders, many=True)
        return Response(serializer.data)


class ClientDeleteItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        model = model_map.get(request.data["model"])

        if not model:
            return Response({"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = model.objects.get(id=request.data["id"], user=request.user)
        except ObjectDoesNotExist:
            return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({}, status=status.HTTP_200_OK)


class ClientAiAnalyzer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.get('data', [])
        data = json.loads(data)
        if not data:
            return Response({"error": "No data for analysis"}, status=400)
        prompt = ""
        if request.data.get("type") == 'loaderA':
            formatted = ", ".join(f"{item['date']}: {item['coupon']}" for item in data)
            prompt = f"""
                You are an AI assistant tasked with analyzing sales data representing coupon usage for a shop. The data is provided in JSON format, where each entry includes a "date" (in YYYY-MM-DD format) and a "coupon" field (indicating the number of coupons used on that date).

                Tasks:
                1. Summarize the trend in coupon usage over the given period, including total usage, distribution, and any notable patterns.
                2. Suggest actionable next steps to improve coupon usage or shop performance based on the data.
                3. Keep the response concise (150-200 words) and professional, suitable for a business report.
                4. Structure the response with sections: Trend Summary and Next Steps.
                
                Data:
                {formatted}
                
                Example Output Structure:
                Trend Summary
                [Summary of coupon usage trends]
                
                Next Steps
                [Actionable recommendations]
                
                Generate the response based on the provided data.
            """
        elif request.data.get("type") == 'loaderB':
            formatted = json.dumps(data)
            prompt = f"""You are an AI assistant tasked with analyzing hierarchical sales data for stores. The data is provided in JSON format, where:
                        - "name" represents the store name at the top level.
                        - Each store has "children", an array of products.
                        - Each product has a "name" and a "sales_volume" (in dollars, referred to as "size" in the data).
                        Use "sales volume" instead of "size" in your response.
                        
                        Tasks:
                        1. Identify the store with the highest total sales volume.
                        2. Identify the product with the highest sales volume across all stores.
                        3. Provide insights or patterns in the data, such as sales distribution or notable trends.
                        
                        Data:
                        { formatted }
                        
                        Instructions:
                        - Provide a concise, professional response in plain text.
                        - Structure the response with sections: Highest Store Sales, Highest Product Sales, Insights.
                        - Calculate totals accurately and explain any notable patterns.
                        - Keep the response under 200 words.
                        
                        Example Output Structure:
                        Highest Store Sales
                        [Store name and total sales volume]
                        
                        Highest Product Sales
                        [Product name, store, and sales volume]
                        
                        Insights
                        [Key observations or trends]"""

        elif request.data.get("type") == 'loaderC':
            formatted = json.dumps(data)
            prompt = f"""You are an AI assistant tasked with generating a concise and professional report based on shop activity data. The data includes daily counts of orders and reviews for a specific shop over a period of time. Your task is to analyze the data and produce a report that summarizes the activity, highlights key trends, and provides insights in a clear, narrative format.

                        Input Data:
                        {formatted}
                        
                        Instructions:
                        1. Write a report in a professional tone, summarizing the shop's activity (orders and reviews) over the given period.
                        2. Include the following:
                           - A brief introduction stating the purpose of the report and the time period covered.
                           - A summary of the total number of orders and reviews.
                           - Key observations or trends (e.g., days with high/low activity, balance between orders and reviews).
                           - A concluding statement with a simple insight or recommendation based on the data.
                        3. Keep the report concise (150-200 words).
                        4. Format the report with clear sections: Introduction, Summary, Observations, and Conclusion.
                        5. Use plain text, suitable for inclusion in a business document.
                        
                        Example Output Structure:
                        Introduction
                        [Brief introduction]
                        
                        Summary
                        [Total orders and reviews, time period]
                        
                        Observations
                        [Key trends or patterns]
                        
                        Conclusion
                        [Insight or recommendation]
                        
                        Generate the report based on the provided data."""


        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json().get("response", "Error.")
        return Response({"summary": result})


class ClientShopsData(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            shop_id = request.data.get('id')
            print(shop_id)
            shop = Shops.objects.get(id=shop_id, user=request.user)
            print(f"Shop found: {shop}")
            if not shop:
                return JsonResponse({'error': 'Shop not found'}, status=400)
            # Query orders
            start = request.data.get('start')
            end = request.data.get('end')
            if start is not None and end is not None:
                start_date = parser.parse(start)
                end_date = parser.parse(end)

                orders_qs = (
                    Order.objects
                    .filter(
                        owner_id=request.user.id,
                        product__shop_id=shop.id,
                        created_at__range=(start_date, end_date)
                    )
                    .annotate(
                        event_type=Value('order', output_field=CharField()),
                        event_date=TruncDate('created_at')
                    )
                    .values('event_date', 'event_type')
                )
                reviews_qs = (
                    Reviews.objects
                    .filter(shop_id=shop.id, owner_id=request.user.id, date__range=(start_date, end_date))
                    .annotate(
                        event_type=Value('review', output_field=CharField()),
                        event_date=TruncDate('date')
                    )
                    .values('event_date', 'event_type')
                )
            else:
                orders_qs = (
                    Order.objects
                    .filter(owner_id=request.user.id, product__shop_id=shop.id)
                    .annotate(
                        event_type=Value('order', output_field=CharField()),
                        event_date=TruncDate('created_at')
                    )
                    .values('event_date', 'event_type')
                )
                print(orders_qs.all())
                reviews_qs = (
                    Reviews.objects
                    .filter(shop_id=shop.id, owner_id=request.user.id)
                    .annotate(
                        event_type=Value('review', output_field=CharField()),
                        event_date=TruncDate('date')
                    )
                    .values('event_date', 'event_type')
                )

            # Combine queries using union
            combined = list(chain(orders_qs, reviews_qs))

            # Aggregate counts
            counts = defaultdict(lambda: {'orders': 0, 'reviews': 0})
            for item in combined:
                print(f"Processing item: {item}")
                date_str = str(item['event_date'])
                # Map 'order' to 'orders' and 'review' to 'reviews'
                event_key = 'orders' if item['event_type'] == 'order' else 'reviews'
                counts[date_str][event_key] += 1

            # Format response
            result = [
                {'date': date, 'orders': data['orders'], 'reviews': data['reviews']}
                for date, data in sorted(counts.items())  # Sort by date
            ]

            if not result:
                return JsonResponse({'message': 'No orders or reviews found', 'data': {}}, status=204)

            return JsonResponse(result, safe=False, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Shop not found'}, status=404)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)