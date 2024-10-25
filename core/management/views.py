from django.shortcuts import render
from product.models import Product



def createProduct(request):
    return render(request, "management/addProduct.html")
