from django.contrib import admin
from .models import (
    Card, CardCategory, UserCard, UserService, UserWork,
    Cart, CartItem, Payment, CardReview, SocialAccount
)

admin.site.register(Card)
admin.site.register(CardCategory)
admin.site.register(UserCard)
admin.site.register(UserService)
admin.site.register(UserWork)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(CardReview)
admin.site.register(SocialAccount)
