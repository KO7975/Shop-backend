from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe


def img_tag(self):

    if self.image:
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    else:
        self.image = "category/photos/box.jpg"
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    perent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # products = models.ManyToManyField('Product', blank=True, related_name='product_desc')
    image= models.ImageField(verbose_name='Category picture', upload_to='category/photos', blank=True, null=True)


    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)


    def __str__(self) -> str:
        return f'{self.name}'
    

    def image_tag(self):
        return img_tag(self)
   
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    image= models.ImageField(verbose_name='Product picture', upload_to='product/photos', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    categoty_id = models.ForeignKey(Category,  on_delete=models.CASCADE,  null=True)
    # stocke = models.ForeignKey('Stock', on_delete=models.CASCADE, blank=True, null=True)
    atr = models.ForeignKey('Attribute', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def image_tag(self):
        return img_tag(self)
   
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    

class  TextProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.value


class  IntegerProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.value


class Attribute(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    int = models.ForeignKey(IntegerProductAttribute, on_delete=models.CASCADE,blank=True, null=True)
    text = models.ForeignKey(TextProductAttribute, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    ptoduct_id = models.OneToOneField(to=Product,  on_delete=models.CASCADE, verbose_name='item')
    quantity = models.IntegerField(null=True,)
    weight = models.DecimalField(decimal_places=3, max_digits=10, null=True, blank=True)
    demensions = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(decimal_places=3, max_digits=10)
    defective = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ptoduct_id.name
