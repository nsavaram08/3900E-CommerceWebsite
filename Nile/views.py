import random

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from Cart.cart import Cart
from Cart.forms import CartAddProductForm
from .forms import OrderCreateForm
from .models import Item, Category, Order, OrderItem, SubCategory
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404


def index(request):
    """View function for home page of site."""
    available_item_ids = Item.objects.filter(availability="a").values_list('id', flat=True)
    randomized_item_ids = random.sample(list(available_item_ids), min(len(available_item_ids), 25))
    recommended_items = Item.objects.filter(id__in=randomized_item_ids)

    context = {
        'recommended_items': recommended_items
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Nile/index.html', context=context)


class ItemCreate(CreateView):
    model = Item
    fields = ['id', 'name', 'description', 'price', 'image', 'quantity', 'category', 'subcategory']


class ItemUpdate(UpdateView):
    model = Item
    fields = ['id', 'name', 'description', 'price', 'image', 'quantity', 'category', 'subcategory']


def ProductDetail(request, pk):
    product = get_object_or_404(Item, pk=pk)
    # set choices for quantity available based on inventory and items in this session's cart
    cart = Cart(request)
    cartquantity = 0
    # if item in cart, subtract the items in the cart from the quantity available
    for item in cart:
        cartproduct = get_object_or_404(Item, id=item['product'].id)
        if product == cartproduct:
            cartquantity = item['quantity']
            break
    if product.quantity - cartquantity > 0:
        choices = [(i, str(i)) for i in range(1, product.quantity - cartquantity + 1)]
    else:  # no items left in inventory for this session
        choices = [(1, 0)]

    cart_product_form = CartAddProductForm(my_choices=choices)
    return render(request, 'Nile/item_detail.html',
                  {'item': product,
                   'subcategory': SubCategory,
                   'cart_product_form': cart_product_form,
                   'cart': cart})


class CategoryDetail(DetailView):
    model = Category

def category_detail(request, category_id):
    category = SubCategory.objects.get(pk=category_id)
    items = Item.objects.filter(subcategory__category=category)
    return render(request, 'Nile/category_detail.html', {'category': category, 'items': items})


class CategoryList(ListView):
    model = Category


@login_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'Nile/admin/order/pdf.html',
                  {'order': order})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'Nile/admin/order/detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.user_id = request.user.id
            order.save()
            print(order.user_id)
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
                # reduce the number of items in inventory based on this sale
                item['product'].quantity = item['product'].quantity - item['quantity']
                item['product'].save()
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id

            return render(request, 'Nile/order_created.html', {'order_id': order.id})
    else:
        form = OrderCreateForm()
    return render(request,
                  'Nile/order_create.html',
                  {'cart': cart, 'form': form})


@login_required
def orders_list(request):
    user = request.user

    orders = Order.objects.filter(user_id=user.id)

    context = {
        'orders': orders
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'Nile/order_list.html', context=context)


def subcategory_detail(request, subcategory_id):
    try:
        subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
        items = Item.objects.filter(subcategory=subcategory, availability='a')

        context = {
            'subcategory': subcategory,
            'items': items,
        }

        return render(request, 'Nile/subcategory_detail.html', context)

    except SubCategory.DoesNotExist:
        raise Http404("SubCategory does not exist")
