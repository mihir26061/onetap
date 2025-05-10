from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import (
    Card, CardCategory, UserCard, UserService, UserWork, Cart, CartItem,
    Payment, CardReview
)
from .serializers import (
    UserSerializer, CardSerializer, CardCategorySerializer,
    UserCardSerializer, UserServiceSerializer, UserWorkSerializer,
    CartSerializer, CartItemSerializer, PaymentSerializer,
    CardReviewSerializer
)

User = get_user_model()

# ------------------ USER ------------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# ------------------ CARD ------------------

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        card = self.get_object()
        reviews = card.reviews.all()
        serializer = CardReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class CardCategoryViewSet(viewsets.ModelViewSet):
    queryset = CardCategory.objects.all()
    serializer_class = CardCategorySerializer


class UserCardViewSet(viewsets.ModelViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ------------------ USER SERVICE & WORK ------------------

class UserServiceViewSet(viewsets.ModelViewSet):
    serializer_class = UserServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserService.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserWorkViewSet(viewsets.ModelViewSet):
    serializer_class = UserWorkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserWork.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ------------------ CART ------------------

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class RemoveFromCartView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]


# ------------------ PAYMENT ------------------

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ------------------ CARD REVIEW ------------------

class CardReviewViewSet(viewsets.ModelViewSet):
    queryset = CardReview.objects.all()
    serializer_class = CardReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)




from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            password=data['password']
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
