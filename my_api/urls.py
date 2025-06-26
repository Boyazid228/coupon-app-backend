
from django.urls import path

import categories.views
from .views import (
    review_list,
    menu_list,
    get_shops,
    get_shop,
    get_coupons,
    getCoupon,
    getHots,
    signup,
    getMarks,
    UserProfileView,
    VlogsView,
    LikesView,
    GetLikesView,
    OrderView,
    MyReviewView,


)
from client.views import (
    ClientItemView,
    ClientProductsView,
    ClientShops,
    ClientReviews,
    ClientDeleteItem,
    ClientLocations,
    ClientOrders,
    ClientAiAnalyzer,
    ClientShopsData
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('reviews/<int:id>/<str:type>/', review_list),
    path('getMenu/', menu_list),
    path('getShops/<int:id>/', get_shops),
    path('getShop/<int:id>/', get_shop),
    path('getCoupons/<int:id>/', get_coupons),
    path('getCoupon/<int:id>/', getCoupon),
    path('hot/', getHots),
    path('seller/', getHots),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', signup),
    path('getMarks/', getMarks),
    path('getUser/', UserProfileView.as_view()),
    path('getVlogs/', VlogsView.as_view()),
    path('setLike/', LikesView.as_view()),
    path('getLike/', GetLikesView.as_view()),
    path('order/', OrderView.as_view()),
    path('getmyreviews/', MyReviewView.as_view()),

    #dashboard
    path('getproducts/', ClientProductsView.as_view()),
    path('getitem/<str:type>/<int:id>/', ClientItemView.as_view()),
    path('get-shops/', ClientShops.as_view()),
    path('get-reviews/', ClientReviews.as_view()),
    path('get-locations/', ClientLocations.as_view()),
    path('get-orders/', ClientOrders.as_view()),
    path('delete-item/', ClientDeleteItem.as_view()),
    path('shop-data/', ClientShopsData.as_view()),

    #ai- Client
    path('ai-analyze/', ClientAiAnalyzer.as_view())






]
