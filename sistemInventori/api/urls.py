from django.urls import path
from .views import BarangListCreateView, PeminjamanListCreateView, AkunListCreateView, StockListCreateView

urlpatterns = [
    path('barang/', BarangListCreateView.as_view(), name='author-list-create'),
    path('peminjaman/', PeminjamanListCreateView.as_view(), name='book-list-create'),
    path('akun/', AkunListCreateView.as_view(), name='book-loan-list-create'),
    path('stock/', StockListCreateView.as_view(), name='book-loan-list-create'),
    # Additional paths for other views or endpoints related to your app...
]
