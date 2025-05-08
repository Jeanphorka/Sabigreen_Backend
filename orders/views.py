from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone

from .models import Order, OrderItem
from products.models import Product

# ดึงรายการคำสั่งซื้อทั้งหมด 
@swagger_auto_schema(
    method='get',
    operation_description="ดึงรายการคำสั่งซื้อทั้งหมด",
    responses={200: openapi.Response(
        description="สำเร็จ",
        examples={
            "application/json": [
                {
                    "id": 1,
                    "order_number": "ORD-20240508-0001",
                    "full_name": "สมชาย เขียวสด",
                    "created_at": "2024-05-08T12:00:00Z",
                    "total_price": 1500.00,
                    "shipping_fee": 60.00,
                    "items": [
                         {
                            "product_id": 1,
                            "product_name": "Uji Matcha 100g",
                            "description": "มัจฉะแท้จากเมืองอุจิ แหล่งต้นกำเนิดมัจฉะ...",
                            "quantity": 2,
                            "price_each": 390.0
                        },
                        {
                            "product_id": 5,
                            "product_name": "Uji Deep Roast Hojicha 250g",
                            "description": "โฮจิฉะสูตรคั่วเข้มจากเมืองอุจิ ให้กลิ่นหอมเข้ม...",
                            "quantity": 1,
                            "price_each": 580.0
                        }
                    ]
                }
            ]
        }
    )}
)
@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all().order_by('-created_at')  

    data = []
    for order in orders:
        items = [
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "description": item.product.description,
                "quantity": item.quantity,
                "price_each": float(item.product.price_thb)
            }
            for item in order.items.all()
        ]
        data.append({
            "id": order.id,
            "order_number": order.order_number,
            "full_name": order.full_name,
            "created_at": order.created_at,
            "total_price": float(order.total_price),
            "shipping_fee": float(order.shipping_fee),
            "items": items
        })

    return Response(data)

# ดูรายละเอียดคำสั่งซื้อจาก order ID
@swagger_auto_schema(
    method='get',
    operation_description="ดูรายละเอียดคำสั่งซื้อจาก order ID",
    responses={
        200: openapi.Response(
            description="ข้อมูลคำสั่งซื้อ",
            examples={
                "application/json": {
                    "id": 1,
                    "order_number": "ORD-20240508-0001",
                    "full_name": "สมชาย เขียวสด",
                    "address": "123 ถนนราชดำเนิน เขตพระนคร กรุงเทพฯ",
                    "email": "somchai@example.com",
                    "phone_number": "0812345678",
                    "delivery_method": "รับหน้าร้าน",
                    "created_at": "2025-05-08T16:17:20.515329Z",
                    "total_price": 1360.0,
                    "shipping_fee": 0.0,
                    "items": [
                        {
                            "product_id": 1,
                            "product_name": "Uji Matcha 100g",
                            "description": "มัจฉะแท้จากเมืองอุจิ แหล่งต้นกำเนิดมัจฉะ...",
                            "quantity": 2,
                            "price_each": 390.0
                        },
                        {
                            "product_id": 5,
                            "product_name": "Uji Deep Roast Hojicha 250g",
                            "description": "โฮจิฉะสูตรคั่วเข้มจากเมืองอุจิ ให้กลิ่นหอมเข้ม...",
                            "quantity": 1,
                            "price_each": 580.0
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(description="ไม่พบคำสั่งซื้อ")
    }
)
@api_view(['GET'])
def get_order_by_id(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'ไม่พบคำสั่งซื้อ'}, status=status.HTTP_404_NOT_FOUND)

    items = [
        {
            "product_id": item.product.id,
            "product_name": item.product.name,
            "description": item.product.description,
            "quantity": item.quantity,
            "price_each": float(item.product.price_thb)
        }
        for item in order.items.all()
    ]

    data = {
        "id": order.id,
        "order_number": order.order_number,
        "full_name": order.full_name,
        "address": order.address,
        "email": order.email,
        "phone_number": order.phone_number,
        "delivery_method": order.delivery_method,
        "created_at": order.created_at,
        "total_price": float(order.total_price),
        "shipping_fee": float(order.shipping_fee),
        "items": items
    }

    return Response(data)

# สร้างคำสั่งซื้อใหม่
@swagger_auto_schema(
    method='post',
    operation_description="สร้างคำสั่งซื้อใหม่",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['full_name', 'address', 'email', 'phone_number', 'delivery_method', 'items'],
        properties={
            'full_name': openapi.Schema(type=openapi.TYPE_STRING, example='สมชาย เขียวสด'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, example='123 ถนนราชดำเนิน เขตพระนคร กรุงเทพฯ'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='somchai@example.com'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example='0812345678'),
            'delivery_method': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=['รับหน้าร้าน', 'จัดส่งทางไปรษณีย์'],
                example='รับหน้าร้าน'
            ),
            'items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    },
                    required=['product_id', 'quantity']
                ),
            ),
        },
    ),
    responses={201: openapi.Response(description="สร้างคำสั่งซื้อสำเร็จ")}
)
@api_view(['POST'])
def create_order(request):
    data = request.data

    order = Order.objects.create(
        full_name=data['full_name'],
        address=data['address'],
        email=data['email'],
        phone_number=data['phone_number'],
        delivery_method=data['delivery_method'],
        shipping_fee=60 if data['delivery_method'] == "จัดส่งทางไปรษณีย์" else 0,
    )

    for item in data.get('items', []):
        product = Product.objects.get(id=item['product_id'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity']
        )

    today_str = timezone.now().strftime('%Y%m%d')
    order.order_number = f"ORD-{today_str}-{order.id:04d}"
    order.save()

    return Response({'message': 'สร้างคำสั่งซื้อสำเร็จ', 'order_id': order.id}, status=status.HTTP_201_CREATED)

# แก้ไขข้อมูลคำสั่งซื้อ (ไม่รวมสินค้า)
@swagger_auto_schema(
    method='put',
    operation_description="แก้ไขข้อมูลคำสั่งซื้อ (ไม่รวมสินค้า)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['full_name', 'address', 'email', 'phone_number', 'delivery_method'],
        properties={
            'full_name': openapi.Schema(type=openapi.TYPE_STRING, example='สมชาย อัปเดตใหม่'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, example='99 ถนนใหม่ เขตบางรัก กรุงเทพฯ'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', example='newemail@example.com'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example='0811111111'),
            'delivery_method': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=['รับหน้าร้าน', 'จัดส่งทางไปรษณีย์'],
                example='จัดส่งทางไปรษณีย์'
            )
        }
    ),
    responses={200: openapi.Response(description="อัปเดตเรียบร้อย"), 404: "ไม่พบคำสั่งซื้อ"}
)
@api_view(['PUT'])
def update_order_info(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'ไม่พบคำสั่งซื้อ'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    order.full_name = data.get('full_name', order.full_name)
    order.address = data.get('address', order.address)
    order.email = data.get('email', order.email)
    order.phone_number = data.get('phone_number', order.phone_number)
    order.delivery_method = data.get('delivery_method', order.delivery_method)

    if order.delivery_method == "จัดส่งทางไปรษณีย์":
        order.shipping_fee = 60
    else:
        order.shipping_fee = 0

    order.save()

    return Response({'message': 'แก้ไขข้อมูลคำสั่งซื้อเรียบร้อยแล้ว'})

# ลบคำสั่งซื้อ
@swagger_auto_schema(
    method='delete',
    operation_description="ลบคำสั่งซื้อโดยใช้ order ID",
    responses={
        200: openapi.Response(description="ลบคำสั่งซื้อเรียบร้อย"),
        404: openapi.Response(description="ไม่พบคำสั่งซื้อ")
    }
)
@api_view(['DELETE'])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'ไม่พบคำสั่งซื้อ'}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response({'message': 'ลบคำสั่งซื้อเรียบร้อยแล้ว'}, status=status.HTTP_200_OK)