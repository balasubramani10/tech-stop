from django.urls import path
from .views import createProduct



urlpatterns = [
    path("create-product/", createProduct,  name="create-product"),

]
