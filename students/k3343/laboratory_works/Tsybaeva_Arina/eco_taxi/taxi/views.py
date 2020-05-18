import datetime
from django.db import models
from django_filters import rest_framework as filters
from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Driver, Order, Client, Storage
from .serializers import (DriverDetailSerializer, DriverListSerializer, OrderCreateSerializer,
                          OrderDetailSerializer, YoungClientSerializer, DriverOrderSerializer,
                          WeekOrderSerializer, TopCategorySerializer, StorageSerializer,
                          TotalTrashSerializer, StorageCreateOrderSerializer)
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ClientFilter, OrderFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
# Create your views here.


class DriverListView(generics.ListAPIView):
    """Вывод списка водителей"""
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DriverDetailView(generics.RetrieveAPIView):
    """Вывод водителя"""
    queryset = Driver.objects.all()
    serializer_class = DriverDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderCreateView(generics.CreateAPIView):
    """Добавление нового заказа"""
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailView(generics.RetrieveAPIView):
    """Вывод заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class YoungListView(generics.ListAPIView):
    """Вывод списка клиентов моложе 40"""
    queryset = Client.objects.all()
    serializer_class = YoungClientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ClientFilter
    filter_backends = (DjangoFilterBackend,)


class DriverOrderView(generics.ListAPIView):
    """Заказы определенного водителя за указанную дату"""
    queryset = Order.objects.all()
    serializer_class = DriverOrderSerializer
    filterset_class = OrderFilter
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [permissions.IsAdminUser]
    #filter_backends = (SearchFilter, OrderingFilter)
    #search_fields = ('data', 'driver__name')


class WeekDayOrderView(generics.ListAPIView):
    """Количество заказов в процентном отношении за каждый день недели"""
    def get_queryset(self):
        total_amount = Order.objects.count()
        order = Order.objects.values('data__week_day').annotate(percent=Count('id')*(100/total_amount)).order_by('data__week_day')
        return order
    serializer_class = WeekOrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TopCategoryView(generics.ListAPIView):
    """Топ 3 часто сдаваемых категории"""
    def get_queryset(self):
        order = Order.objects.values('category__name').annotate(amount=Count('id')).order_by('-amount')[:3]
        return order
    serializer_class = TopCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StorageClientView(generics.ListAPIView):
    """Объем мусора, забранный у клиентов"""
    def get_queryset(self):
        trash = Order.objects.values('category__name').annotate(amount=Sum('mass'))
        return trash
    serializer_class = TopCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class StorageView(generics.ListAPIView):
    """Объем мусора на складе"""
    def get_queryset(self):
        trash = Storage.objects.values('order__category').annotate(amount=Sum('order__mass'))
        return trash
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAdminUser]


class ToFabricTrashView(generics.ListAPIView):
    """Отчет за месяц"""

    def get_queryset(self):
        today = datetime.date.today()
        trash_client = Order.objects.filter(data__month=today.month).aggregate(total=Sum('mass'))
        trash_storage = Storage.objects.filter(order__data__month=today.month).aggregate(total=Sum('order__mass'))
        total_client = Order.objects.filter(data__month=today.month).count()
        total_money = Order.objects.filter(data__month=today.month).aggregate(money=Sum('cost'))
        passed = trash_client['total']-trash_storage['total']
        trash = [{"total_to_fabric": passed, "total_from_client": trash_client['total'], "total_client": total_client, "total_money" :total_money['money']}]
        return trash
    serializer_class = TotalTrashSerializer
    permission_classes = [permissions.IsAdminUser]


class DriverCreateView(generics.CreateAPIView):
    """Добавление водителя"""
    serializer_class = DriverDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class DriverDeleteView(generics.DestroyAPIView):
    """Удаление водителя"""
    queryset = Driver.objects.all()
    serializer_class = DriverDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class OrderStorageCreateView(generics.CreateAPIView):
    """Добавление заказа на склад"""
    serializer_class = StorageCreateOrderSerializer
    permission_classes = [permissions.IsAdminUser]

class OrderStorageDeleteView(generics.DestroyAPIView):
    """Списание заказа со склада"""
    queryset = Storage.objects.all()
    serializer_class = StorageCreateOrderSerializer
    permission_classes = [permissions.IsAdminUser]


