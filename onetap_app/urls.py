from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CardViewSet, CardCategoryViewSet,
    UserCardViewSet, UserServiceViewSet, UserWorkViewSet,
    CartView, AddToCartView, RemoveFromCartView,
    PaymentViewSet, CardReviewViewSet
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'cards', CardViewSet, basename='card')
router.register(r'categories', CardCategoryViewSet, basename='category')
router.register(r'user-cards', UserCardViewSet, basename='user-card')
router.register(r'services', UserServiceViewSet, basename='service')
router.register(r'works', UserWorkViewSet, basename='work')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'reviews', CardReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='cart-remove'),
]

urlpatterns += [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


from .views import SignupView

urlpatterns += [
    path('auth/signup/', SignupView.as_view(), name='signup'),
]
