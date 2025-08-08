from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import mixins, filters, views
from .models import Bag
from .serializers import BagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


@api_view(['GET', ])
def bag_list(request):
    bags = Bag.objects.all()
    category = request.GET.get('category')
    if category:
        bags = bags.filter(category__name=category)

    search = request.GET.get('search')
    if search:
        bags = bags.filter(
            Q(name__icontains=search) | Q(color__icontains=search)
        )

    price_gt = request.GET.get('price_gt')
    if price_gt:
        bags = bags.filter(price__gt=price_gt)

    price_lt = request.GET.get('price_lt')
    if price_lt:
        bags = bags.filter(price__lt=price_lt)

    ordering = request.GET.get('ordering')
    if ordering:
        bags = bags.order_by(ordering)

    paginator = LimitOffsetPagination()
    paginator.page_size = 2
    paginated_bags = paginator.paginate_queryset(bags, request)

    serializer = BagSerializer(paginated_bags, many=True)
    data = {
        'data':serializer.data,
        'count':len(bags),
        'status':status.HTTP_200_OK
    }
    return paginator.get_paginated_response(data)

@api_view(['POST',])
def bag_create(request):
    serializer = BagSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['GET',])
def bag_detail(request, pk):
    try:
        bag = Bag.objects.get(id=pk)
    except Bag.DoesNotExist:
        return Response({'status':status.HTTP_400_BAD_REQUEST})
    serializer = BagSerializer(bag)
    data = {
        'data':serializer.data,
        'status':status.HTTP_200_OK
    }
    return Response(data)

@api_view(['PUT',])
def bag_update(request, pk):
    bag = Bag.objects.get(id=pk)
    serializer = BagSerializer(bag, dat=request.data)
    if serializer.save():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['PATCH',])
def bag_update(request, pk):
    bag = Bag.objects.get(id=pk)
    serializer = BagSerializer(bag, dat=request.data, partial=True)
    if serializer.save():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['DELETE',])
def bag_delete(request, pk):
    try:
        bag = Bag.objects.get(id=pk)
    except Bag.DoesNotExist:
        return Response({'status':status.HTTP_400_BAD_REQUEST})
    bag.delete()
    return Response({'status':status.HTTP_200_OK})


### cbv
# class ListCreateApiView(APIView):
#     def get(self, request):
#         bags = Bag.objects.all()
#         category = request.GET.get('category')
#         if category:
#             bags = bags.filter(category__name=category)
#
#         search = request.GET.get('search')
#         if search:
#             bags = bags.filter(
#                 Q(name__icontains=search) | Q(color__icontains=search)
#             )
#
#         price_gt = request.GET.get('price_gt')
#         if price_gt:
#             bags = bags.filter(price__gt=price_gt)
#
#         price_lt = request.GET.get('price_lt')
#         if price_lt:
#             bags = bags.filter(price__lt=price_lt)
#
#         ordering = request.GET.get('ordering')
#         if ordering:
#             bags = bags.order_by(ordering)
#
#         paginator = LimitOffsetPagination()
#         paginator.page_size = 3
#         paginated_bags = paginator.paginate_queryset(bags, request)
#
#         serializer = BagSerializer(paginated_bags, many=True)
#         data = {
#             'data': serializer.data,
#             'count':len(bags),
#             'status':status.HTTP_200_OK
#         }
#         return paginator.get_paginated_response(data)
#
#     def post(self, request):
#         serializer = BagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK})
#         return Response({'status':status.HTTP_400_BAD_REQUEST})
#
# class DeleteDetailUpdateApiView(APIView):
#     def get(self, request, pk):
#         try:
#             bag = Bag.objects.get(id=pk)
#         except Bag.DoesNotExist:
#             return Response({'status':status.HTTP_400_BAD_REQUEST})
#         serializer = BagSerializer(bag)
#         data = {
#             'data':serializer.data,
#             'status':status.HTTP_200_OK
#         }
#         return Response(data)
#
#     def put(self, request, pk):
#         bag = Bag.objects.get(id=pk)
#         serializer = BagSerializer(bag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK})
#         return Response({'status':status.HTTP_400_BAD_REQUEST})
#
#     def patch(self, request, pk):
#         bag = Bag.objects.get(id=pk)
#         serializer = BagSerializer(bag, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK})
#         return Response({'status':status.HTTP_400_BAD_REQUEST})
#
#     def delete(self, request, pk):
#         try:
#             bag = Bag.objects.get(id=pk)
#         except Bag.DoesNotExist:
#             return Response({'status':status.HTTP_400_BAD_REQUEST})
#         bag.delete()
#         return Response({'status':status.HTTP_200_OK})
#


### genericapiview
#
# class ListCreateApiView(GenericAPIView):
#     queryset = Bag.objects.all()
#     serializer_class = BagSerializer
#
#     def get(self, request):
#         bag = Bag.objects.all()
#
#         category = request.GET.get('category')
#         if category:
#             bag = bag.filter(category__name=category)
#
#         search = request.GET.get('search')
#         if search:
#             bag = bag.filter(
#                 Q(name__icontains=search) | Q(color__icontains=search)
#             )
#
#         price_gt = request.GET.get('price_gt')
#         if price_gt:
#             bag = bag.filter(price__gt=price_gt)
#
#         price_lt = request.GET.get('price_lt')
#         if price_lt:
#             bag = bag.filter(price__lt=price_lt)
#
#         ordering = request.GET.get('ordering')
#         if ordering:
#             bag = bag.order_by(ordering)
#
#         paginator = LimitOffsetPagination()
#         paginator.page_size = 2
#         paginated_bag = paginator.paginate_queryset(bag, request)
#
#         serializer = BagSerializer(paginated_bag, many=True)
#
#         data = {
#             'data':serializer.data,
#             'count':len(bag),
#             'status':status.HTTP_200_OK
#         }
#         return paginator.get_paginated_response(data)
#
#     def post(self, request):
#         serializer = BagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK})
#         return Response({'status':status.HTTP_400_BAD_REQUEST})
#
# class DetailDeleteUpdateApiView(GenericAPIView):
#     queryset = Bag.objects.all()
#     serializer_class = BagSerializer
#
#     def get(self, request, pk):
#         bag = Bag.objects.get(id=pk)
#         return bag
#
#     def get(self, request, pk):
#         bag = Bag.objects.get(pk=pk)
#         serializer = BagSerializer(bag)
#         data = {
#             'data':serializer.data,
#             'status':status.HTTP_200_OK
#         }
#         return Response(data)
#
#     def put(self, request, pk):
#         bag = Bag.objects.get(id=pk)
#         serializer = BagSerializer(bag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status':status.HTTP_200_OK})
#         return Response({'status':status.HTTP_400_BAD_REQUEST})
#
#     def patch(self, request, pk):
#         bag = Bag.objects.get(id=pk)
#         serializer = BagSerializer(bag, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': status.HTTP_200_OK})
#         return Response({'status': status.HTTP_400_BAD_REQUEST})
#
#     def delete(self, request, pk):
#         try:
#             bag = Bag.objects.get(pk=pk)
#         except Bag.DoesNotExist:
#             return Response({'status':status.HTTP_400_BAD_REQUEST})
#         bag.delete()
#         return Response({'status':status.HTTP_200_OK})
#

# mixins
# class ListCreateApiView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
#     queryset = Bag.objects.all()
#     serializer_class = BagSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['category','price' ]
#     search_fields = ['name']
#     ordering_fields = ['name', 'price']
#     ordering = ['price']
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class DetailDeleteUpdateApiPKView(mixins.UpdateModelMixin,
#                             mixins.DestroyModelMixin,
#                             mixins.RetrieveModelMixin,
#                             GenericAPIView):
#     queryset = Bag.objects.all()
#     serializer_class = BagSerializer
#
#     def get(self, request, pk, *args, **kwargs):
#         return self.retrieve(request, pk=pk)
#
#     def put(self, request, pk, *args, **kwargs):
#         return self.update(request, pk=pk)
#
#     def patch(self, request, pk, *args, **kwargs):
#         return self.partial_update(request, pk=pk)
#
#     def delete(self, request, pk, *args, **kwargs):
#         return self.destroy(request, pk=pk)




