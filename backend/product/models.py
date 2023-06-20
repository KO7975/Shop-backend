from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    perent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField('Product', blank=True, related_name='product_desc')
    image= models.ImageField(verbose_name='Category picture', upload_to='category/photos', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    image= models.ImageField(verbose_name='Product picture', upload_to='product/photos', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    categoty_id = models.ForeignKey(Category,  on_delete=models.CASCADE,  null=True)
    stocke = models.OneToOneField(to='Stock', on_delete=models.CASCADE, blank=True,  null=True)
    atr = models.ManyToManyField('Attribute', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

class  TextProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    attribute_id = models.ForeignKey('Attribute', on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.value


class  IntegerProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    attribute_id = models.ForeignKey('Attribute', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.value


class Attribute(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    ptoduct_id = models.OneToOneField(to=Product,  on_delete=models.CASCADE, verbose_name='item')
    quantity = models.IntegerField(null=True)
    weight = models.DecimalField(decimal_places=3, max_digits=10)
    demensions = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(decimal_places=3, max_digits=10)
    defective = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ptoduct_id.name
