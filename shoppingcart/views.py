from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from shoppingcart.models import Category, Store, Product, Order, Item
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re


USER_RE = re.compile(r"^[a-zA-Z0-9]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)
        
PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return USER_RE.match(password)  
        
EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")   
def valid_email(email):
    return EMAIL_RE.match(email)


def homepage(request):
    store = Store.objects.get(subdomain = request.subdomain)
    if request.method == 'GET':
        try: 
            user = request.session['user'] #if user already logged-in
            login(request,user)
            return redirect('/products/')
        except:
            return render_to_response('home.html', 
                    {'store_name': store.name, 
                        },
                    RequestContext(request))
    else: #POST
        user = authenticate(username = request.POST['username'], 
                            password = request.POST['password'])
        if user:
            login(request, user)
            request.session['user'] = user
            return redirect('/products/')
        else:
            error_message = "No user was found.  Please check your username/password and try again."
            return render_to_response('home.html', 
                {'store_name': store.name, 
                'error_message': error_message},
                RequestContext(request))

def create_user(request):
    store = Store.objects.get(subdomain = request.subdomain)
    if request.method == 'GET': 
        return render_to_response('create_user.html', 
                {'store_name': store.name,
                 }, RequestContext(request))
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm = request.POST['confirm']
        email = request.POST['email']
        empty_field_error = invalid_username_error = invalid_password_error = \
            invalid_email_error = different_passwords_error = ""
        if not all([username, first_name, last_name, password, email]):
            empty_field_error = "All fields must be completed."
            return render_to_response('create_user.html',
                {'store_name': store.name,
                'empty_field_error': empty_field_error,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}, 
                context_instance=RequestContext(request))
        if not valid_username(username):
            invalid_username_error = "Username must be between 3-20 alphanumeric characters"
        if not valid_password(password):
            invalid_password_error = "Password must be between 3-20 characters."
        if not valid_email(email):
            invalid_email_error = "That does not appear to be a valid_email."
        if password != confirm:
            different_passwords_error = "Your passwords do not match."
        if User.objects.get(username=username):
            invalid_username_error = "That username already exists."
        if any([invalid_username_error, invalid_password_error,
                        invalid_email_error, different_passwords_error]):
            return render_to_response('create_user.html',
                {'store_name': store.name,
                'invalid_username_error': invalid_username_error,
                'invalid_password_error': invalid_password_error,
                'invalid_email_error': invalid_email_error,
                'different_passwords_error': different_passwords_error,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}, 
                context_instance=RequestContext(request))
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.orders = {}
            user.save()
            request.session['user'] = user
            return redirect('/products/')

def changeuser(request):
    logout(request)
    return redirect('/home/')

def log_out(request):
    store = Store.objects.get(subdomain = request.subdomain)
    logout(request)
    return render_to_response('logout.html',
            {'store_name': store.name,
            })

def products(request):
    store = Store.objects.get(subdomain = request.subdomain)
    item_added_message = ""
    store_products = Product.objects.filter(store_name=store.id)
    if request.method == 'POST': #load catalog page with "item added"
        # try:
        #     if new_quant <= 0 or (float(new_quant) != int(new_quant)):
        #         print "Neg or not-integer"
        #         raise ValueError
        #     new_quant = int(new_quant)
        # except ValueError:
        #     return render_to_response('catalog.html', 
        #         {'store_name' : store.name, 
        #         'store_products' : store_products,
        #         'not_a_number' : '%s is not a valid amount.'%new_quant},
        #         context_instance=RequestContext(request))
        cart = get_cart(request)
        add_to_cart(request, cart, store)
        request.session.modified = True
        item_added_message = "Shopping cart updated"
    return render_to_response('catalog.html', 
                {'store_name': store.name, 
                'store_products': store_products,
                'item_added_message': item_added_message}, 
                context_instance=RequestContext(request))

def detail(request, product_internal_id):
    product = Product.objects.get(internal_id = product_internal_id)
    item_added_message = ""
    if request.method == 'POST':
        cart = get_cart(request)
        store = Store.objects.get(subdomain = request.subdomain)
        add_to_cart(request, cart, store) 
        item_added_message = "Shopping cart updated"
    return render_to_response('product_detail.html',
                        {'p' : product,
                        'item_added_message' : item_added_message,},
                        context_instance=RequestContext(request))

def shoppingcart(request):
    #load page of all shopping cart items
    store = Store.objects.get(subdomain = request.subdomain)
    cart = get_cart(request)
    number_of_items = count_items(cart)
    if request.method == 'POST':
        cart = changeQuantities(request, cart)
        number_of_items = count_items(cart)
        if 'checkout' in request.POST:
            return redirect('/checkout/')
    return render_to_response('shoppingcart.html', 
            {'store_name': store.name, 
            'cart' : cart,
            'number_of_items' : number_of_items,},
             context_instance=RequestContext(request))



def checkout(request):
    store = Store.objects.get(subdomain = request.subdomain)
    cart = get_cart(request)
    if cart == {}:
        return redirect('/products/')   
    try:
        order = Order(user = request.session['user'], store = store)
        order.save()
    except KeyError:
        return redirect('/home/', 
                    {'error_message' : "Please sign in"}) #!!!
    for product, key in cart.iteritems():
        i = Item(product = product, 
                 quantity = key,
                 order = order
                 )
        i.save()
    request.session['cart'] = cart = {}
    return render_to_response('checkout.html', 
            {'store_name': store.name,
            })

def orderhistory(request):
    store = Store.objects.get(subdomain = request.subdomain)
    try:
        user = request.session['user']
    except:
        return redirect('/home/')
    order_history_list = Order.objects.filter(user = user, store=store.id)
    items_by_order = {}
    for order in order_history_list:
        items_by_order[order] = Item.objects.filter(order = order)
    return render_to_response('orderhistory.html',
            {'store_name': store.name,
             'user': user,
             'items_by_order' : items_by_order,
             'order_history_list' : order_history_list,
            })

def location(request):
    store = Store.objects.get(subdomain = request.subdomain)
    address = "%s, %s, %s, %s"%(store.address, store.city, 
                                store.state, store.zipcode)
    return render_to_response('location.html',
            {'store_name':store.name,
             'address' : address})


def get_cart(request):
    '''gets cart if it exists, otherwise initializes it as empty dict'''
    try:
        cart = request.session['cart']
    except:
        cart = request.session['cart'] = {}
    return cart

def add_to_cart(request, cart, store):
    for product in Product.objects.filter(store_name=store.id):
        if unicode(product.id) in request.POST and int(request.POST[unicode(product.id)]) != 0:
            try:
                cart[product] += int(request.POST[unicode(product.id)])
            except KeyError:
                cart[product] = int(request.POST[unicode(product.id)])
    return cart

def changeQuantities(request, cart):
    '''removes or changes quantities of items in cart'''
    to_be_deleted = []
    for product in cart:
        new_qty = int(request.POST[unicode(product.id)])
        if new_qty == 0:
            to_be_deleted.append(product)
        cart[product] = new_qty
    if to_be_deleted:
        for product in to_be_deleted:
            del cart[product]
    return cart

def count_items(cart):
    number_of_items = 0
    for key, value in cart.iteritems():
        number_of_items += value
    return number_of_items
