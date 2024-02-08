from .cart import Cart
from .cart2 import CartApi


def cart(request):
    return {'cart': CartApi(request)}
