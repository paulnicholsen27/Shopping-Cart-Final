#from django.utils import unittest
from models import Store, Product, Category, Order, Item
from django.test import TestCase
from django.test.client import Client

class PageChecks(TestCase):
    fixtures = ['shoppingcart_testdata.json']

    def setup(self):
        self.client = Client()
        #self.urls = 'ogstore2.urls.py'
        self.client.defaults['HTTP_HOST'] = 'nerdgasm.paulstore.com:8000'

    def test_home(self):
        request.subdomain = 'nerdgasm'
        response=self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        pass

    def test_cart(self):
        pass

    def test_checkout(self):
        pass

    def test_orderhistory(self):
        pass

    def test_create_user(self):
        pass

    def test_location(self):
        pass

    def test_changeuser(self):
        pass