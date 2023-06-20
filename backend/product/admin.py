from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Stock, Attribute, TextProductAttribute, IntegerProductAttribute


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('products',)

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated', 'image_tag')
    search_fields = ('name', )
    prepopulated_fields = {"slug": ("name",)}

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="60" />')



@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display= ('name', 'quantity', 'price', 'defective', 'created', 'updated' )

    def name(self, obj):
        return obj.ptoduct_id.name



@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display= ('name', )


@admin.register(TextProductAttribute)
class TextProductAttributeAdmin(admin.ModelAdmin):
    list_display = ( 'value', 'created', 'updated' )


@admin.register(IntegerProductAttribute)
class IntegerProductAttributeAdmin(admin.ModelAdmin):
    list_display = ( 'value', 'created', 'updated' )



# admin.site.register(Category, CategoryAdmin)
