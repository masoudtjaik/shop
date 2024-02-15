from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *
# from user.views import *
app_name = 'api'
urlpatterns = [
    path("add_to_cart/", AddToCartView.as_view(), name="Add to cart"),
    path("address/", ShowAddress.as_view(), name="address"),
    path("subtitle/order", SubtitleOrder.as_view(), name="subtitle_order"),
    path("date/order", DateOrder.as_view(), name="date_order"),
    path("order/items/<int:get_id>", OrderItems.as_view(), name="order_items"),
    # path("remove-from-cart/", RemoveFromCartView.as_view(), name="Remove from cart"),
    # path("update-cart/", UpdateCart.as_view(), name="Update cart"),
    # path("get-total-price/", CalculateTotal.as_view(), name="Calculate total price"),
    # path("get-discount/", CalculateDiscount.as_view(), name="Calculate discount"),
    # path("submit-order/", SubmitOrder.as_view(), name="Submit order"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)