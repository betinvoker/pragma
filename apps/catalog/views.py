from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def catalog_list(request):
    items = Item.objects.all()
    return render(request, 'catalog/client_list.html', {'items': items})

@login_required
def manager_catalog(request):
    items = Item.objects.all()
    return render(request, 'catalog/manager_list.html', {'items': items})


@login_required
def client_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for item_id, qty in cart.items():
        try:
            item = Item.objects.get(id=item_id)
            line = item.price * qty
            items.append({'item': item, 'qty': qty, 'line': line, 'id': item_id})
            total += line
        except Item.DoesNotExist:
            pass
    return render(request, 'catalog/cart.html', {'cart_items': items, 'total': total})


@login_required
def cart_add(request):
    if request.method == 'POST':
        item_id = str(request.POST.get('item_id'))
        qty = int(request.POST.get('qty', 1))
        cart = request.session.get('cart', {})
        cart[item_id] = cart.get(item_id, 0) + qty
        request.session['cart'] = cart
    return redirect('client_cart')


@login_required
def cart_remove(request):
    if request.method == 'POST':
        item_id = str(request.POST.get('item_id'))
        cart = request.session.get('cart', {})
        cart.pop(item_id, None)
        request.session['cart'] = cart
    return redirect('client_cart')