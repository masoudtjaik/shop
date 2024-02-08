from django.urls import path, include
from . import views

app_name = 'order'

urlpatterns = [
    path('<int:id>/', views.ADDTOCART.as_view(), name='add_cart'),
    path('delete/<slug:slug>/', views.DELETECART.as_view(), name='delete_cart'),
    path('create_address/', views.CreateAddress.as_view(), name="create_address"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('date/', views.DateOrder.as_view(), name="date_order"),
    path('subtitle/', views.SubtitleOrder.as_view(), name="subtitle_order"),
    path('items/<int:pk>', views.ShowOrderItem.as_view(), name="order_item"),
    path('cart/remove/<int:id>/', views.DeleteCart.as_view(), name="remove"),
    path('order/', views.OrderCreateView.as_view(), name="create_order"),
    # path('categories',views.ShowCategorys.as_view(),name='categories'),
]
