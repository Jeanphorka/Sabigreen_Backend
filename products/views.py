from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from django.http import HttpResponse


def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price_thb),
                'weight_grams': product.weight_grams,
                'description': product.description,
                'in_stock': product.in_stock,
                'tea_type': product.tea_type.name if product.tea_type else None,
                'image_url': product.image.url if product.image else None
            })
        return JsonResponse(data, safe=False)

