from django import template
import locale

register = template.Library()

@register.filter(name='currency')
def currency(value):
    try:
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL,'')
    loc = locale.localeconv()
    return locale.currency(value, loc['currency_symbol'], grouping=True)

@register.filter(name='item_total')
def item_total(price, quantity):
    return price * quantity

@register.filter(name='total_cost')
def total_cost(db):
    total = 0
    for key, value in db:
        total += (value * key.price)
    return total

@register.filter(name='lookup')
def lookup(d, key):
    return d[key]

@register.filter(name='order_total')
def order_total(orderhistory):
    total = 0
    for item in orderhistory:
        total += item.total_price
    return total
