from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer

@swagger_auto_schema(method='get', responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: ProductSerializer()})
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
