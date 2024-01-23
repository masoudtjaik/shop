from django.urls import path,include
from . import views
app_name='products'

urlpatterns = [
    path('<int:pk>/',views.Products.as_view(),name='product'),
    path('detail/<slug:slug>/',views.DetailProduct.as_view(),name='detail'),
    path('comment/<int:get_id>/',views.CommentAdd.as_view(),name='comment'),
    path('like/<int:get_id>/',views.LikeAdd.as_view(),name='like'),
    path('search/',views.Search.as_view(),name='search'),
    # path('categories',views.ShowCategorys.as_view(),name='categories'),
]
