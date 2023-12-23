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

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'

class PeminjamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peminjaman
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'  
