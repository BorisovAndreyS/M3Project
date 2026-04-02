from django.contrib import admin

from products.models import Product, Category, Review, ProductSpecification, SpecificationType


class ProductSpecificationInLine(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    autocomplete_fields = ['spec_type']


@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'stock', 'price', 'is_active']
    list_filter = ['name', 'category']
    search_fields = ['name']
    ordering = ['-stock']
    inlines = (ProductSpecificationInLine,)


admin.site.register(Category)
admin.site.register(Review)
