import datetime

from django.template.response import TemplateResponse
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum

# from user.authentication import JWTAuthentication
from .serializers import *
# from ...models import DiscountCoupon, Cart, Order
# from user.models import User
# from core.views import BasicViewMixin
from products.models import Product
from order.cart import Cart
from order.cart2 import CartApi
from rest_framework import status
from account.models import Address
from order.models import *


class AddToCartView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = AddToCartViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        quantity = serializer.validated_data.get('quantity')
        product = Product.objects.get(pk=pk)
        cart = request.COOKIES.get('cart', None)
        my_cart = CartApi(request)

        if product.inventory > 0:
            # discounted_price = serializer.validated_data.get('discounted_price')
            # if discounted_price != "None":
            #     cart_dict = {'pk': pk, 'name': name, 'price': discounted_price, 'inventory': quantity}
            # else:
            #     cart_dict = {'pk': pk, 'name': name, 'price': price, 'inventory': quantity}

            # if not cart:
            #     cart = f'{cart_dict}'
            # else:
            #     cart += f';{cart_dict}'
            # cart2 = Cart(request)
            # cart_info = cart2.add(product, quantity)
            carts = my_cart.add(name, quantity, product)
            # if cart_info is False:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            if carts is False:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            response = my_cart.get_response()

            return response
        else:
            return Response({'product': 'not enough'}, status=HTTP_406_NOT_ACCEPTABLE)


class RemoveFromCartView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RemoveFromCartViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        cart = self.get_user_cart(self.request, total=False)
        temp_str = ''
        for product in cart:
            product['image'] = ""
            if product['pk'] == pk:
                del product
                continue
            product['name'] = product['name'].encode('utf-8')
            if len(temp_str) == 0:
                temp_str = f'{product}'
            else:
                temp_str += f';{product}'

        response = Response({'cart': 'ok'})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("cart", temp_str, expires=expires_string)

        return response

    def get_user_cart(self, request, total):
        pass


#
#
# class UpdateCart(APIView, BasicViewMixin):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = UpdateCartSerializer
#
#     def get(self, request):
#         cart = self.get_user_cart(self.request, total=False)
#         if cart:
#             serializer_ = self.serializer_class(data=cart, many=True)
#             serializer_.is_valid(raise_exception=True)
#             return Response(serializer_.data)
#         else:
#             return Response({'cart': 'empty'})
#
#     def patch(self, request):
#         serializer_ = self.serializer_class(data=request.data, partial=True)
#         serializer_.is_valid(raise_exception=True)
#
#         pk = serializer_.validated_data['pk']
#         count = serializer_.validated_data['count']
#         cart = self.get_user_cart(self.request, total=False)
#         temp_str = ''
#         for product in cart:
#             product['image'] = ""
#             if product['pk'] == pk:
#                 c = Product.objects.get(pk=pk)
#                 if c.count >= count:
#                     product['count'] = count
#                 else:
#                     return Response({'error': 'count'}, status=HTTP_406_NOT_ACCEPTABLE)
#             product['name'] = product['name'].encode('utf-8')
#             if len(temp_str) == 0:
#                 temp_str = f'{product}'
#             else:
#                 temp_str += f';{product}'
#
#         response = Response({'cart': 'ok'})
#         expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
#         expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
#         response.set_cookie("cart", temp_str, expires=expires_string)
#
#         return response
#
#
# class CalculateTotal(APIView, BasicViewMixin):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = CalculateTotalSerializer
#
#     def get(self, request):
#         totals = self.get_user_cart(self.request, total=True)
#         if totals:
#             serializer_ = self.serializer_class(data=totals)
#             serializer_.is_valid(raise_exception=True)
#             return Response(serializer_.data)
#         else:
#             return Response({'cart': 'empty'})
#
#
# class CalculateDiscount(APIView, BasicViewMixin):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication,]
#     serializer_class = CalculateDiscountSerializer
#     discount_amount = 0
#     shipping_price = 0
#
#     def post(self, request):
#         serializer_ = self.serializer_class(data=request.data)
#         serializer_.is_valid(raise_exception=True)
#         CalculateDiscount.shipping_price = serializer_.validated_data['shipping_price']
#         if not serializer_.validated_data['code'] == "کد تخفیف":
#             coupon_code = DiscountCoupon.objects.filter(code=serializer_.validated_data['code'])
#         else:
#             response = Response({'value': 0})
#             return response
#         if coupon_code:
#             username = self.request.session.get('username', None)
#             user = User.objects.get(username=username)
#             for code in coupon_code:
#                 if code.discount_is_active and code.owner == user:
#                     if code.discount.amount_of_percentage_discount:
#                         CalculateDiscount.discount_amount = code.discount.amount_of_percentage_discount
#                         response = Response({'value': CalculateDiscount.discount_amount})
#                     else:
#                         CalculateDiscount.discount_amount = code.discount.amount_of_non_percentage_discount
#                         response = Response({'value': CalculateDiscount.discount_amount})
#                     code.is_deleted = True
#                     code.save()
#                     return response
#         raise NotFound('invalid code')
#
#     def get(self, request):
#         total_price = self.get_user_cart(self.request, total=True)['total_price']
#         discount = CalculateDiscount.discount_amount
#         shipping_price = CalculateDiscount.shipping_price
#         if discount < 100:
#             final_price = (total_price + shipping_price) * (1-discount/100)
#             discount = (total_price + shipping_price) * (discount/100)
#         else:
#             final_price = (total_price + shipping_price) - discount
#         return Response({'total_price': total_price, 'discount': discount, 'shipping_price': shipping_price,
#                          'final_price': final_price})
#
#
# class SubmitOrder(APIView, BasicViewMixin):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubmitOrderSerializer
#
#     def post(self, request):
#         username = self.request.session.get('username', None)
#         user = User.objects.get(username=username)
#
#         item = self.get_user_cart(self.request, total=False)
#         for product in item:
#             p = Product.objects.get(pk=product['pk'])
#             p.count -= 1
#             p.save()
#             del product['image']
#
#         serializer_ = self.serializer_class(data=request.data)
#         serializer_.is_valid(raise_exception=True)
#         shipping_price = serializer_.validated_data['shipping_price']
#         address_id = serializer_.validated_data['address_id']
#         total_price = serializer_.validated_data['total_price']
#
#         cart = Cart(customer=user, item=item, shipping_price=shipping_price, address_id=address_id,
#                     total_price=total_price)
#         cart.save()
#
#         status = 'ثبت شده'
#
#         order = Order(cart=cart, status=status)
#         order.save()
#
#         response = Response({'order_id': order.pk})
#         response.set_cookie("cart", '')
#         return response


class ShowAddress(APIView):

    def get(self, request):
        address_list = Address.objects.filter(user=request.user)
        paginator = Paginator(address_list, 10)

        page = request.GET.get('page')
        try:
            addresses = paginator.page(page)
        except PageNotAnInteger:
            addresses = paginator.page(1)
        except EmptyPage:
            addresses = paginator.page(paginator.num_pages)

        serializer_data = AddressSerializer(instance=addresses, many=True)

        context = {
            'object_list': serializer_data.data,
            'addresses': addresses
        }
        return TemplateResponse(request, 'account/address.html', context, status=status.HTTP_200_OK)

    # return TemplateResponse(request, 'account/address.html', context)


class SubtitleOrder(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        paginator = Paginator(orders, 10)

        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        serializer_data = SubtitleOrderSerializer(instance=orders, many=True)
        context = {
            'object_list': serializer_data.data,
            'page_obj': orders
        }
        return TemplateResponse(request, 'order/subtitle_order.html', context, status=status.HTTP_200_OK)


class DateOrder(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        paginator = Paginator(orders, 10)

        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        serializer_data = DateOrderSerializer(instance=orders, many=True)
        context = {
            'object_list': serializer_data.data,
            'page_obj': orders
        }
        return TemplateResponse(request, 'order/date_order.html', context, status=status.HTTP_200_OK)


class OrderItems(APIView):
    def get(self, request, get_id):
        products = Product.objects.prefetch_related('product_orderitem').filter(product_orderitem__order__id=get_id)
        products_with_quantity = products.annotate(total_quantity=Sum('product_orderitem__count'))

        paginator = Paginator(products_with_quantity, 10)

        page = request.GET.get('page')
        try:
            products_with_quantity = paginator.page(page)
        except PageNotAnInteger:
            products_with_quantity = paginator.page(1)
        except EmptyPage:
            products_with_quantity = paginator.page(paginator.num_pages)

        serializer_data = ProductSerializer(instance=products_with_quantity, many=True)
        context = {
            'object_list': serializer_data.data,
            'page_obj': products_with_quantity
        }
        return TemplateResponse(request, 'order/order_item.html', context, status=status.HTTP_200_OK)
