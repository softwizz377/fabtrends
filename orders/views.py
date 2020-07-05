from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from coupons.forms import CouponApplyForm
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RequestRefundForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='/login/')
def order_create(request):
    global order
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            #cart.clear()
            #order_created.delay(order.id)
            # set the order in the session
            #request.session['order_id'] = order.id
        #return redirect(reverse('payment:process'))
        return render(request, 'pay.html', {'order': order})
        #return redirect('/')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})
    #return render(request, 'orders/order/create.html', {'cart': cart,
                                                       # 'form': form})

def order_created(request):
    
    return render(request, 'orders/order/created.html', {'form': form})
    #return render(request, 'orders/order/create.html', {'cart': cart,
                                                       # 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'orders/order/detail.html',
                  {'order': order,'coupon_apply_form': coupon_apply_form})


@staff_member_required
def admin_order_pdf(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0] + '/css/pdf.css')])
    return response


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RequestRefundForm()
        context = {
            'form': form
        }
        return render(self.request, "refund.html", context)

    def post(self, *args, **kwargs):
        form = RequestRefundForm(self.request.POST)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(order_id=order_id)
                order.refund_requested = True
                order.save()

                #store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request has been submitted and our team will get in contact with you")
                return redirect('refund-view')

            except ObjectDoesNotExist:
                messages.warning(self.request, "This order does not exists")
                return redirect('refund-view')
