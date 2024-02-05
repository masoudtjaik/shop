SABAD_SHOP = 'sabad'
from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SABAD_SHOP)
        if not cart:
            cart = self.session[SABAD_SHOP] = {}
        self.cart = cart

    def __iter__(self):
        product_id = self.cart.keys()
        products = Product.objects.filter(id__in=product_id)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total'] = int(item['price']) * item['numbers']
            yield item

    def __len__(self):
        return sum(item['numbers'] for item in self.cart.values())

    def add(self, product, numbers):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'numbers': 0, 'name': str(product.name), 'price': str(product.price_discount)}
            print('hello')
        # print('cart', self.cart[product_id])
        if self.cart[product_id]['numbers'] + int(numbers) > product.inventory:
            return False
        self.cart[product_id]['numbers'] += int(numbers)

        self.save()
        print('cart', self.cart[product_id])

    def delete(self, product):
        del self.cart[str(product.id)]
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * int(item['numbers']) for item in self.cart.values())
