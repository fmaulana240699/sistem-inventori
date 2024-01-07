from rest_framework import serializers
from .models import Barang, Peminjaman, Akun, Stock

class AkunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Akun
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password) 
        instance.save()
        return instance  
     
    
class AkunNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Akun
        fields = ('nama_lengkap',)

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'

class BarangNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = ('nama_barang',)

class PeminjamanSerializer(serializers.ModelSerializer):
    id_akun = AkunNameSerializer(read_only=True)
    id_barang = BarangNameSerializer(read_only=True)
    class Meta:
        model = Peminjaman
        fields = '__all__'      

class CreatePeminjamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peminjaman
        fields = ['tanggal_peminjaman','tanggal_pengembalian','id_akun','id_barang']               

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'  
