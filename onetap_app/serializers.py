from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Card, CardCategory, UserCard, UserService, UserWork,
    Cart, CartItem, Payment, CardReview
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'digital_profile', 'links', 'contact_info', 'social_media_links']


class CardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCategory
        fields = ['id', 'name']


class CardSerializer(serializers.ModelSerializer):
    category = CardCategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'category', 'price', 'details', 'owner']


class UserCardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    card = CardSerializer()

    class Meta:
        model = UserCard
        fields = [
            'id', 'user', 'card', 'business_card_name',
            'theme', 'style', 'cover_photo',
            'main_heading', 'sub_heading'
        ]


class UserServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserService
        fields = ['id', 'user', 'service_detail']
        read_only_fields = ['user']


class UserWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWork
        fields = ['id', 'user', 'work_detail']
        read_only_fields = ['user']


class CartItemSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    card_id = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(), source='card', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'card', 'card_id', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['user']


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    card = CardSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'user', 'card', 'status', 'paid_at']
        read_only_fields = ['user']


class CardReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = CardReview
        fields = ['id', 'card', 'reviewer', 'star', 'description', 'reviewed_at']
        read_only_fields = ['reviewer']
