from rest_framework import generics
from .models import Barang, Peminjaman, Akun, Stock
from .serializers import BarangSerializer, PeminjamanSerializer, AkunSerializer, StockSerializer

class BarangListCreateView(generics.ListCreateAPIView):
    queryset = Barang.objects.all()
    serializer_class = BarangSerializer

class PeminjamanListCreateView(generics.ListCreateAPIView):
    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

class AkunListCreateView(generics.ListCreateAPIView):
    queryset = Akun.objects.all()
    serializer_class = AkunSerializer

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer    
