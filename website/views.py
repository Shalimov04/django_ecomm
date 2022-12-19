from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import CheckOutForm
import secrets
import string
from django.contrib.auth.models import Group, Permission
from api.models import *


def index(request):
    try:
        categories = Category.objects.all()
    except:
        categories = []
    rows_count = len(categories) // 3
    if len(categories) > rows_count * 3: rows_count += 1
    rows = []
    for i in range(0, rows_count):
        temp = []
        for j in range(3):
            try:
                temp.append(categories[i*3+j])
            except:
                break
        rows.append(temp)
    return render(request, 'index.html', {'categories': rows})


def all_items(request, cat_pk, cond_pk):
    current = {
        'category': cat_pk,
        'condition': cond_pk,
    }
    items = Item.objects.filter(count__gte=1).all()

    try:
        if cat_pk > 0:
            items = items.filter(category=Category.objects.get(pk=cat_pk)).all()

        if cond_pk in ('new', 'used', 'discount'):
            items = items.filter(condition=cond_pk.upper()).all()

    except:
        items = []


    categories = Category.objects.all()
    return render(request, 'category.html', {'items': items, 'categories': categories, 'current': current})


def item(request, item_pk):
    try:
        item = Item.objects.get(pk=item_pk)
    except Item.DoesNotExist:
        return redirect('/')

    if request.method == 'POST':
        item = Item.objects.get(pk=item_pk)
        count = item.count
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        ordered_item, created = OrderedItem.objects.get_or_create(order=order, item=item)
        if int(request.POST['quantity']) < count: count = request.POST['quantity']
        ordered_item.count = count
        ordered_item.cost = float(ordered_item.count) * ordered_item.item.price
        ordered_item.save()
        try:
            cat = item.category.pk
        except:
            cat = 0
        return redirect(f'/items/{cat}/all')

    return render(request, 'item.html', {'item': item})


def about(request):
    return render(request, 'about.html')


def cart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    if len(OrderedItem.objects.filter(order=order).all()) >= 1:
        not_empty = True
    else:
        not_empty = False

    context = {'order': order, 'not_empty': not_empty}
    return render(request, 'cart.html', context)


def checkout(request):
    form = CheckOutForm()
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    try:
        address = PickupAddress.objects.get().details
    except:
        address = 'Уточните по телефону'

    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            order.completed = True
            alphabet = string.ascii_letters + string.digits
            order_token = ''.join(secrets.choice(alphabet) for i in range(10))
            order.token = order_token
            order.save()

            #уменьшение кол-ва товаров
            ordered_items = OrderedItem.objects.filter(order=order)
            for item in ordered_items:
                item.item.count -= item.count
                item.item.save()

            customer.name = name
            customer.email = email
            customer.save()
            response = HttpResponseRedirect(f'/order/{order_token}')
            response.delete_cookie('device')
            return response

    context = {'order': order, 'address': address, 'form': form}
    return render(request, 'checkout.html', context)


def delete(request, item_pk):
    try:
        item = Item.objects.get(pk=item_pk)
        device = request.COOKIES['device']
        customer = Customer.objects.get(device=device)
        order = Order.objects.get(customer=customer, completed=False)
        OrderedItem.objects.filter(order=order, item=item).delete()
    except:
        pass
    return redirect('/cart')


def cat(request):
    for group in Group.objects.all():
        permissions = group.permissions.all()
        for perm in permissions:
            print(f'["{perm.codename}", "{perm.name}"]')
    return render(request, 'kitten.html')


def order(request, order_token):
    order = Order.objects.get(token=order_token)
    items = OrderedItem.objects.filter(order=order).all()
    context = {'order': order, 'items': items}
    return render(request, 'order.html', context=context)

