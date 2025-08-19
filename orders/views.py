from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'create_order.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        cart_items = user.cart_items.select_related('product').all()
        for item in cart_items:
            item.total = item.product.price * item.quantity
        total_price = sum(item.total for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = user.cart_items.select_related('product').all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        cart_items.delete()
        return redirect('order-success-url')



class OrderSuccess(TemplateView):
    template_name = 'order_success.html'