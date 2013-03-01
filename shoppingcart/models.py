from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subdomain = models.CharField(max_length=255, null=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 2, choices = [('WA', 'Washington'), 
        ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('FL', 'Florida'), 
        ('WY', 'Wyoming'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), 
        ('NM', 'New Mexico'), ('NA', 'National'), ('NC', 'North Carolina'), 
        ('ND', 'North Dakota'), ('NE', 'Nebraska'), ('NY', 'New York'), 
        ('RI', 'Rhode Island'), ('NV', 'Nevada'), ('GU', 'Guam'), 
        ('CO', 'Colorado'), ('CA', 'California'), ('GA', 'Georgia'), 
        ('CT', 'Connecticut'), ('OK', 'Oklahoma'), ('OH', 'Ohio'), 
        ('KS', 'Kansas'), ('SC', 'South Carolina'), ('KY', 'Kentucky'), 
        ('OR', 'Oregon'), ('SD', 'South Dakota'), ('DE', 'Delaware'), 
        ('DC', 'District of Columbia'), ('HI', 'Hawaii'), ('PR', 'Puerto Rico'),
        ('TX', 'Texas'), ('LA', 'Louisiana'), ('TN', 'Tennessee'), 
        ('PA', 'Pennsylvania'), ('VA', 'Virginia'), ('VI', 'Virgin Islands'), 
        ('AK', 'Alaska'), ('AL', 'Alabama'), ('AS', 'American Samoa'), 
        ('AR', 'Arkansas'), ('VT', 'Vermont'), ('IL', 'Illinois'), 
        ('IN', 'Indiana'), ('IA', 'Iowa'), ('AZ', 'Arizona'), ('ID', 'Idaho'), 
        ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), 
        ('UT', 'Utah'), ('MO', 'Missouri'), ('MN', 'Minnesota'), 
        ('MI', 'Michigan'), ('MT', 'Montana'), ('MP', 'Northern Mariana Islands'), 
        ('MS', 'Mississippi')])
    zipcode = models.CharField(max_length=9)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'stores'
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,
                                    blank=True,default=0.00)
    image = models.CharField(max_length=50, default="imagenotfound.jpeg")
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    store_name = models.ForeignKey(Store, blank = True, null = True)
    internal_id = models.CharField(max_length = 9, unique=True, null=True)
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User)
    order_date = models.DateTimeField(auto_now_add=True)
    store = models.ForeignKey(Store)

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']
    def __unicode__(self):
        return unicode(self.order_date.strftime("%B %d, %Y"))

class Item(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order)

    class Meta:
        db_table = 'items'
        ordering = ['order']

    def __unicode__(self):
        return str(self.order.order_date)


    def total_price(self):
        return self.quantity*self.product.price
    total_price = property(total_price)