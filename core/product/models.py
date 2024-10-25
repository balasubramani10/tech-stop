from django.db import models
from base.models import BaseModel
from django.utils.text import slugify



class ProductManufacturer(BaseModel):
    name = models.CharField(max_length= 256, null= False, blank= False, unique= True)
    description = models.TextField(max_length= 1024, null= True, blank= True, default= " ")
    logo = models.ImageField(upload_to="product/manufacturer_logo", null= True, blank= True)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(ProductManufacturer,self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class ProductBrand(BaseModel):
    manufacturer = models.ForeignKey(ProductManufacturer , on_delete= models.CASCADE, related_name="brand")
    name = models.CharField(max_length=256, null = False, blank= False, unique= True)
    logo = models.ImageField(upload_to="product/brand_logo", null= True, blank= True)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(ProductBrand,self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class ProductCategory(BaseModel):
    slug = models.SlugField(unique=True, null = True, blank = True)
    name = models.CharField(max_length= 64, null= False, blank= False, unique= True)
    logo = models.ImageField(upload_to="product/category_logo", null= True, blank= True)
    icon = models.ImageField(upload_to="product/category_icon", null= True, blank= True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory,self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class ProductVariantType(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(ProductVariantType,self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class ProductVariantValue(BaseModel):
    variant_type = models.ForeignKey(ProductVariantType, on_delete=models.CASCADE, related_name='variant')
    value = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(ProductVariantValue,self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.variant_type.name}: {self.value}"


class Product(BaseModel):
    manufacturer = models.ForeignKey(ProductManufacturer, on_delete=models.CASCADE, related_name='product')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='product')
    categories = models.ManyToManyField(ProductCategory, related_name='product')
    name = models.CharField(max_length=512)
    description = models.TextField()
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    variant = models.ForeignKey(ProductVariantValue, on_delete=models.CASCADE, related_name='product_variant')
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, null = True, blank = True)
    def save(self, *args , **kwargs):
        self.slug = slugify(self.name)
        super(ProductVariant,self).save(*args, **kwargs)
    def get_price(self):
        return self.price_override if self.price_override is not None else self.product.retail_price
    def __str__(self):
        return f"{self.product.name} - {self.variant.value}"

class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "images")
    image = models.ImageField(upload_to="product/images")
    def __str__(self):
        return self.product.name