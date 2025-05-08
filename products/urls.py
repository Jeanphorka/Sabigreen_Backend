from django.urls import path
from .views import product_list , product_detail ,health_check


urlpatterns = [
    path('all', product_list, name='product-list'),
    path('<int:pk>', product_detail, name='product-detail'),
    path('health', health_check),
]
