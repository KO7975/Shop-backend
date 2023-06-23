from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import(
    Category,
    Product,
    Stock,
    Attribute,
    TextProductAttribute,
    IntegerProductAttribute,
    Like,
    DisLike,
    )


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at')

#     def name(self, obj):
#         return obj.user.username
    
# @admin.register(DisLike)
# class DisLikeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at')

#     def name(self, obj):
#         return obj.user.username


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    prepopulated_fields = {"slug": ("name",)}
    # filter_horizontal = ('products',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'created', 'updated', 'image_tag')
    search_fields = ('name', )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display= ('name', 'quantity', 'defective', 'created', 'updated' )

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
