from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

@swagger_auto_schema(
    method='get',
    operation_summary="ดึงรายการสินค้า",
    operation_description="ดึงรายการสินค้า มี type ทั้งหมด [Tea Whisk, Matcha Stirring Bowl, genmaicha ,hojicha ,matcha]",
    responses={
        200: openapi.Response(
            description="รายการสินค้า",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "type": "matcha",
                        "name": "Uji Matcha 100g",
                        "weight_grams": 100,
                        "price_thb": "390.00",
                        "description": "มัจฉะแท้จากเมืองอุจิ แหล่งต้นกำเนิดมัจฉะที่เก่าแก่...",
                        "in_stock": 50,
                        "image": None
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_description="ดึงรายการสินค้า",
    operation_summary="ดึงข้อมูลสินค้ารายตัวตาม ID",
    responses={
        200: openapi.Response(
            description="รายการสินค้า",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "type": "matcha",
                        "name": "Uji Matcha 100g",
                        "weight_grams": 100,
                        "price_thb": "390.00",
                        "description": "มัจฉะแท้จากเมืองอุจิ แหล่งต้นกำเนิดมัจฉะที่เก่าแก่...",
                        "in_stock": 50,
                        "image": None
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def product_detail(request, pk):
    """
    ดึงข้อมูลสินค้ารายตัวตาม ID
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'ไม่พบสินค้า'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

# API สำหรับเรียกดูสินค้าประเภทชา
@swagger_auto_schema(
    method='get',
    operation_summary="เรียกดูสินค้าประเภทชา",
    operation_description="แสดงรายการสินค้าทุกชนิดที่เป็นชา เช่น matcha, hojicha, genmaicha",
    responses={200: ProductSerializer(many=True)},
)
@api_view(['GET'])
def get_tea_products(request):
    tea_keywords = ['matcha', 'hojicha', 'genmaicha']  # กลุ่มชาเขียว
    teas = Product.objects.filter(type__name__in=tea_keywords)
    serializer = ProductSerializer(teas, many=True)
    return Response(serializer.data)

# API สำหรับเรียกดูสินค้าประเภทอุปกรณ์
@swagger_auto_schema(
    method='get',
    operation_summary="เรียกดูสินค้าประเภทอุปกรณ์ชงชา",
    operation_description="แสดงรายการสินค้าประเภทอุปกรณ์ เช่น Tea Whisk, Matcha Stirring Bowl",
    responses={200: ProductSerializer(many=True)},
)
@api_view(['GET'])
def get_tool_products(request):
    tool_keywords = ['Tea Whisk', 'Matcha Stirring Bowl']  # กลุ่มอุปกรณ์
    tools = Product.objects.filter(type__name__in=tool_keywords)
    serializer = ProductSerializer(tools, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='get', auto_schema=None)
@api_view(['GET'])
def health_check(request):
    return Response({"message": "Backend is alive"}, status=status.HTTP_200_OK)
    
    
