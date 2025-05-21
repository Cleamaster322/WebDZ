from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Brand
from .serializers import BrandSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_csrf_token(request):
    token = get_token(request)
    return Response({'csrf_token': token})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def test(request):
    return Response({'test': 123321})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def test1(request):
    name = request.data.get('name','default value')
    return Response({'name': name})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test2(request):
    print(request.user)
    return Response({'test': 123321})

# class CsrfToken(APIView):
#     def get(self,request):
#         token = get_token(request)
#         return JsonResponse({'csrf_token': token})

class BrandPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

# Добавить пагинацию, фильтрацию, сортровку
class BrandListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # get all brands

    def get(self, request, *args, **kwargs):
        brands = Brand.objects.filter()

        # filter by name
        name = request.GET.get('name')
        if name:
            brands = brands.filter(name__icontains=name)

        # sort
        ordering = request.GET.get('ordering')
        if ordering:
            brands = brands.order_by(ordering)

        paginator = BrandPagination()
        paginated_brands = paginator.paginate_queryset(brands, request)
        serializer = BrandSerializer(paginated_brands, many=True)
        serializer_class = BrandSerializer(brands, many=True)
        return paginator.get_paginated_response(serializer.data)


    # create new brand
    def post(self, request, *args, **kwargs):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# brand by id
class BrandDetailAPIView(APIView):
    # get brand by id
    def get(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer_class = BrandSerializer(brand, many=False)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.filter()
            serializer = BrandSerializer(brand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update not full data brand by id
    def patch(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer = BrandSerializer(brand, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # delete brand by id
    def delete (self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


