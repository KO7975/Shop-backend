from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from authentication.models import User


def img_tag(self):

    if self.image:
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    else:
        self.image = "category/photos/box.jpg"
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    perent_id = models.ForeignKey('self', on_delete=models.CASCADE,  blank=True, related_name='children')
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
    price = models.DecimalField(decimal_places=3, max_digits=10, null=True, blank=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_products')
    dislikes = models.ManyToManyField(User,through='DisLike', related_name='disliked_product', blank=True)
    atr = models.ForeignKey('Attribute', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def image_tag(self):
        return img_tag(self)
   
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DisLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"  


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on Comment {self.comment.id}"
    

class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dislike by {self.user.username} on Comment {self.comment.id}"




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
    defective = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ptoduct_id.name
