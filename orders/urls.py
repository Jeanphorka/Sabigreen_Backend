from django.urls import path
from .views import create_order , list_orders , get_order_by_id , update_order_info , delete_order

urlpatterns = [
    path('create', create_order, name='create-order'),
    path('all', list_orders, name='list-orders'),
    path('<int:order_id>', get_order_by_id , name='get-order-by-id'), 
    path('update/<int:order_id>', update_order_info, name='update-order-info'), 
    path('delete/<int:order_id>', delete_order, name='delete-order'),
]