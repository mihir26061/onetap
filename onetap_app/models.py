from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User with extended fields
class User(AbstractUser):
    digital_profile = models.TextField(blank=True)
    links = models.TextField(blank=True)  # can be JSON or comma-separated
    contact_info = models.TextField(blank=True)
    social_media_links = models.TextField(blank=True)  # can be JSON or comma-separated

    def __str__(self):
        return self.username


# Social Auth for login/signup via Google, Facebook, Apple
class SocialAccount(models.Model):
    PROVIDER_CHOICES = (
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('apple', 'Apple'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_id = models.CharField(max_length=100)  # external provider ID
    created_at = models.DateTimeField(auto_now_add=True)


class CardCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Card(models.Model):
    category = models.ForeignKey(CardCategory, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f"Card {self.id} - {self.owner.username}"


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cards')
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    business_card_name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    cover_photo = models.ImageField(upload_to='cover_photos/')
    main_heading = models.CharField(max_length=200)
    sub_heading = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.business_card_name


class UserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    service_detail = models.TextField()

    def __str__(self):
        return f"Service for {self.user.username}"


class UserWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='works')
    work_detail = models.TextField()

    def __str__(self):
        return f"Work for {self.user.username}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    paid_at = models.DateTimeField(auto_now_add=True)


class CardReview(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.PositiveIntegerField()  # out of 5
    description = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} - {self.star} Stars"
