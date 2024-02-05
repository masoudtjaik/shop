from django.urls import path, include
from . import views

app_name = 'order'

urlpatterns = [
    path('<int:id>/', views.ADDTOCART.as_view(), name='add_cart'),
    path('delete/<slug:slug>/', views.DELETECART.as_view(), name='delete_cart'),
    path('create_address/', views.CreateAddress.as_view(), name="create_address"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('cart/', views.CartView.as_view(), name="cart"),
    # path('categories',views.ShowCategorys.as_view(),name='categories'),
]
