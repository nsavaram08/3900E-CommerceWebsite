import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
# Add PAYMENT METHOD and ADDRESS when we get to the point we introduce shopping cart sessions
# All the USER and USER_LOGIN information should be included in the django USER model

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    # foreign key to the category table
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, null=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.RESTRICT, null=True, blank=True)


    ITEM_AVAILABILITY = (
        ('a', 'Available'),
        ('o', 'Out of Stock'),
    )

    availability = models.CharField(
        max_length=1,
        choices=ITEM_AVAILABILITY,
        blank=True,
        default='a',
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

    def get_absolute_url(self):
        """Returns the URL to access a particular item instance."""
        return reverse('item_detail', args=[str(self.id)])


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

    def get_absolute_url(self):
        """Returns the URL to access a particular category instance."""
        return reverse('category_detail', args=[str(self.id)])


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Order(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_user')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Item,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
