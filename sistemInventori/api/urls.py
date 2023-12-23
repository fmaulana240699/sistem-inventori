from django.urls import path
from .views import UserLogoutView, UserLoginView, ApprovalListCreateView, BarangListCreateView, BarangDeleteView, BarangUpdateView, PeminjamanListCreateView, AkunListCreateView, AkunDeleteView, AkunUpdateView, StockListAPIView, PengembalianListCreateView

urlpatterns = [
    path('barang/', BarangListCreateView.as_view(), name='barang-list-create'),
    path('barang/delete/', BarangDeleteView.as_view(), name='barang-delete'),
    path('barang/<int:pk>/', BarangUpdateView.as_view(), name='barang-update'),
    path('peminjaman/', PeminjamanListCreateView.as_view(), name='peminjaman-list-create'),
    path('pengembalian/', PengembalianListCreateView.as_view(), name="pengembalian-barang"),
    path('approval/', ApprovalListCreateView.as_view(), name="approval-peminjaman"),
    path('akun/', AkunListCreateView.as_view(), name='akun-list-create'),
    path('akun/delete/', AkunDeleteView.as_view(), name='barang-delete'),
    path('akun/<int:pk>/', AkunUpdateView.as_view(), name='barang-update'),
    path('stock/', StockListAPIView.as_view(), name='stock-list'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    
]
