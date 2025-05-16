from django.urls import path
from .views import product_list , product_detail ,health_check ,get_tea_products, get_tool_products


urlpatterns = [
    path('all', product_list, name='product-list'),
    path('<int:pk>', product_detail, name='product-detail'),
    path('tea', get_tea_products),
    path('tools', get_tool_products),
    path('health', health_check),
]
