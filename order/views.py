from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView, ListView, DetailView
from django.views import View
from .models import OrderItem, Order
from products.models import Product
from django.contrib import messages
from .cart import Cart
from .cart2 import CartApi
from account.models import Address
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView


# Create your views here.


class ADDTOCART(View):
    print('hello')

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.product = None
    #     self.number = None

    def setup(self, request, *args, **kwargs):
        self.number = request.GET.get("number")
        self.product = Product.objects.get(pk=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, id):

        if self.number:
            self.add_to_cart(request, self.number)
            return redirect('products:detail', self.product.slug)
        else:
            messages.success(request, 'number is empty ', 'danger')
            return redirect('products:detail', self.product.slug)

    def post(self, request, id):
        self.add_to_cart(request, 1)
        return redirect('products:detail', self.product.slug)

    def add_to_cart(self, request, number):
        print('masoudddd meysammmmm')
        if self.product.inventory < int(number):
            messages.success(request, f'This amount is not available in the warehouse. '
                                      f'The inventory is : {self.product.inventory}', 'danger')
            return redirect('products:detail', self.product.slug)

        cart = CartApi(request)
        cart_info = cart.add(self.product.name, number, self.product)
        if cart_info is False:
            messages.success(request, f'This amount is not available in the warehouse. '
                                      f'The inventory is  : {self.product.inventory}', 'danger')
            return redirect('products:detail', self.product.slug)
        messages.success(request, 'add to cart done  ', 'success')
        print('session', request.session.get('sabad'))
        cart.get_response()
        print(cart)
        # request.session['username'] = username


class DELETECART(View):

    def get(self, request, slug, ):
        cart = Cart(request)
        print('session', request.session.get('sabad'))
        cart.delete(Product.objects.get(slug=slug))
        # if slug_status == 'home':
        #     return redirect('core:home')
        product = Product.objects.get(slug=slug)
        return redirect('order:cart')


class CartView(View):
    template_class = 'order/cart.html'

    def get(self, request):
        cart = CartApi(request)
        if request.user.is_authenticated:
            address = Address.objects.filter(user=request.user)
        else:
            address = None
        return render(request, self.template_class, {'cart': cart, 'address': address})


class OrderDetailView(LoginRequiredMixin, View):
    temlate_class = 'order/checkout.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        cart = Cart(request)
        return render(request, self.temlate_class, {'order': order, 'cart': cart})


class OrderCreateViews(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        # order = Order(user=request.user)
        # order.save()
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])

            # order_item = OrderItem(order = order,Product = item['product'], quantity =item['quantity'])
            # order_item.save()

        return redirect('orders:order_detail', order.id)


class CreateAddress(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            return redirect("core:home")
        country = request.POST.get("country")
        city = request.POST.get("city")
        street = request.POST.get("street")
        state = request.POST.get("state")
        Address.objects.create(user=user, country=country, city=city, street=street, state=state)
        return redirect("order:checkout")


class CheckoutView(CartView):
    template_class = 'order/checkout.html'


class DateOrder(LoginRequiredMixin, ListView):
    template_name = 'order/date_order.html'
    model = Order
    paginate_by = 4


class SubtitleOrder(ListView):
    template_name = 'order/subtitle_order.html'
    model = Order
    paginate_by = 4
    queryset = Order.objects.archive()


class ShowOrderItem(LoginRequiredMixin, ListView):
    template_name = 'order/order_item.html'
    model = OrderItem
    paginate_by = 4

    def get_queryset(self):
        return OrderItem.objects.select_related('order').filter(order__id=self.kwargs['pk'])


class DeleteCart(View):
    def get(self, request, id):
        cart = CartApi(request)
        response = cart.delete(id)
        return response


class OrderCreateView(LoginRequiredMixin, APIView):
    def get(self, request):
        cart = CartApi(request)
        order = Order.objects.create(user=request.user, is_paid=True)
        # order = Order(user=request.user)
        # order.save()

        for item in cart:
            OrderItem.objects.create(user=request.user, order=order, product=item['product'], count=item['quantity'])
            # order_item = OrderItem(order = order,Product = item['product'], quantity =item['quantity'])
            # order_item.save()
        response = cart.delete()
        return response
