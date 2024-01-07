import qrcode
import base64
from io import BytesIO
from datetime import datetime
from .models import Barang, Peminjaman, Akun, Stock
from .serializers import BarangSerializer, PeminjamanSerializer, AkunSerializer, StockSerializer, CreatePeminjamanSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .custom_permissions import IsAdmin, IsItSupport, IsKaryawan, IsRoleExtend
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.forms.models import model_to_dict
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime
from django.http import JsonResponse
import json
from django.core.serializers import serialize



class BarangListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport | IsRoleExtend]

    queryset = Barang.objects.all()
    serializer_class = BarangSerializer

    def post(self, request):
        data = request.data
        serializer = BarangSerializer(data=data)
        if serializer.is_valid():
            qr_data = serializer.validated_data

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=4
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Get QR code data as a string
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code data as bytes
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            qr_data_instance = serializer.save(qr_code=base64_image)

            #Update stock
            try:
                update_stock = Stock.objects.get(nama_barang=qr_data['jenis_barang'])
                update_stock.jumlah_barang = update_stock.jumlah_barang + 1
                update_stock.save()
            except Stock.DoesNotExist:
                Stock.objects.update_or_create(id_barang=qr_data_instance.id, nama_barang=qr_data['jenis_barang'], jumlah_barang=1)
            
            return Response(BarangSerializer(qr_data_instance).data, status=201)
        return Response(serializer.errors, status=400)


class BarangDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport]

    def delete(self, request):
        barang_id = request.data.get('id')

        try:
            barang = Barang.objects.get(id=barang_id)
            barang.delete()
            return Response({'message': 'Barang berhasil dihapus'}, status=204)
        except Barang.DoesNotExist:
            return Response({'message': 'Barang tidak ditemukan'}, status=404)

class BarangUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport]

    def patch(self, request, pk):
        try:
            barang = Barang.objects.get(pk=pk)
            serializer = BarangSerializer(barang, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Barang.DoesNotExist:
            return Response({'message': 'Barang tidak ditemukan'}, status=404)        

class PeminjamanListPerUserAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport ]

    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

    def get(self, request, pk):
        try:
            list_peminjaman = Peminjaman.objects.filter(id_akun=pk)
            serialized_data = serialize("json", list_peminjaman)
            serialized_data = json.loads(serialized_data)
            return Response(serialized_data, status=200)
        except Barang.DoesNotExist:
            return Response({'message': 'Peminjaman tidak ditemukan'}, status=404)   

class PeminjamanListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport | IsKaryawan]

    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

class PeminjamanListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport | IsKaryawan]

    queryset = Peminjaman.objects.all()
    serializer_class = CreatePeminjamanSerializer

    def post(self, request):
        data = request.data
        serializer = CreatePeminjamanSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tanggal_pengembalian_str = validated_data["tanggal_pengembalian"].strftime('%Y-%m-%d')
            tanggal_peminjaman_str = validated_data["tanggal_peminjaman"].strftime('%Y-%m-%d')
            durasi = datetime.strptime(tanggal_pengembalian_str, '%Y-%m-%d').date() - datetime.strptime(tanggal_peminjaman_str, '%Y-%m-%d').date()
            validated_data["durasi_peminjaman"] = durasi.days
            validated_data["status_peminjaman"] = "Waiting Approval"

            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)            
                
class ApprovalListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport]

    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer

    def post(self, request):
        data = request.data
        if data["approval"] == "setuju":
            try:
                approved = Peminjaman.objects.get(id=data["id"])
                approved.status_peminjaman = "Dipinjam"
                approved.save()

                # need to update status barang
                barang = Barang.objects.get(id=approved.id_barang.id)
                barang.status_barang = "Dipinjam"
                barang.save()

                # need to update stock barang
                update_stock = Stock.objects.get(nama_barang=barang.jenis_barang)
                update_stock.jumlah_barang = update_stock.jumlah_barang - 1
                update_stock.save() 

                return Response({'message': 'Peminjaman berhasil disetujui'}, status=204)
            except Akun.DoesNotExist:
                return Response({'message': 'Peminjaman gagal disetujui'}, status=404) 
        else:
            approved = Peminjaman.objects.get(id=data["id"])
            approved.status_peminjaman = "Ditolak"
            approved.save()         

            return Response({'message': 'Peminjaman berhasil ditolak'}, status=204)

class PengembalianListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport | IsKaryawan]

    queryset = Peminjaman.objects.all()
    serializer_class = PeminjamanSerializer
    
    def put(self, request):
        data = request.data
        try:
            approved = Peminjaman.objects.get(id=data["id"])
            approved.status_peminjaman = "Done"
            approved.save()

            # need to update status barang
            barang = Barang.objects.get(id=approved.id_barang.id)
            barang.status_barang = "Ready"
            barang.save()

            # need to update stock barang
            update_stock = Stock.objects.get(nama_barang=barang.jenis_barang)
            update_stock.jumlah_barang = update_stock.jumlah_barang + 1
            update_stock.save()

            return Response({'message': 'Barang berhasil dikembalikan'}, status=204)
        except:
            return Response({'message': 'Error ketika mengembalikan'}, status=500)

class AkunListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]    
    queryset = Akun.objects.all()
    serializer_class = AkunSerializer     

class AkunDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request):
        akun_id = request.data.get('id')

        try:
            barang = Akun.objects.get(id=akun_id)
            barang.delete()
            return Response({'message': 'Akun berhasil dihapus'}, status=204)
        except Akun.DoesNotExist:
            return Response({'message': 'Akun tidak ditemukan'}, status=404)

class AkunUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        try:
            akun = Akun.objects.get(pk=pk)
            serializer = AkunSerializer(akun, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data["password"] = make_password(request.data["password"])
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Akun.DoesNotExist:
            return Response({'message': 'Akun tidak ditemukan'}, status=404)    

class StockListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsItSupport]
        
    queryset = Stock.objects.all()
    serializer_class = StockSerializer     

class UserLoginView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = Akun.objects.get(username=request.data['username'])
        

        return Response({
            'access': str(serializer.validated_data["access"]),
            'refresh': str(serializer.validated_data["refresh"]),
            'user_data': model_to_dict(user_id)
        }, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
  
            token = request.data["refresh"]
            blacklist = RefreshToken(token)
            blacklist.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid token or logout failed'}, status=status.HTTP_400_BAD_REQUEST)
